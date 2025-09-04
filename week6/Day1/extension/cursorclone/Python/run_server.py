import os
import sys
import json
import asyncio
from typing import TypedDict, Annotated
from collections import defaultdict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
app = FastAPI()

# --- SERVER-SIDE MEMORY ---
# We use a defaultdict that creates a new list for any new conversation_id
conversation_histories = defaultdict(list)

# --- WORKSPACE CONTEXT ---
WORKSPACE_ROOT = os.environ.get("WORKSPACE_ROOT", "")

# --- LANGGRAPH LOGIC (Unchanged) ---
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]

tavily_tool = TavilySearch(max_results=3)

@tool("read_file", return_direct=False)
def tool_read_file(path: str) -> str:
    """Read a UTF-8 text file from the workspace given a relative path like 'src/index.ts'."""
    try:
        base = WORKSPACE_ROOT or os.getcwd()
        abs_path = os.path.abspath(os.path.join(base, path))
        if WORKSPACE_ROOT and not abs_path.startswith(os.path.abspath(WORKSPACE_ROOT)):
            return "Access outside of workspace is not allowed"
        if not os.path.exists(abs_path):
            return f"File not found: {path}"
        with open(abs_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {e}"

@tool("write_file", return_direct=False)
def tool_write_file(path: str, content: str) -> str:
    """Write UTF-8 text to a file in the workspace at 'path'. Creates directories if needed."""
    try:
        base = WORKSPACE_ROOT or os.getcwd()
        abs_path = os.path.abspath(os.path.join(base, path))
        if WORKSPACE_ROOT and not abs_path.startswith(os.path.abspath(WORKSPACE_ROOT)):
            return "Access outside of workspace is not allowed"
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote file: {path}"
    except Exception as e:
        return f"Error writing file {path}: {e}"

@tool("search_workspace", return_direct=False)
def tool_search_workspace(query: str, start_path: str = ".") -> str:
    """Search all text files under 'start_path' for occurrences of 'query'. Returns a list of files with matches."""
    base = WORKSPACE_ROOT or os.getcwd()
    root = os.path.abspath(os.path.join(base, start_path))
    if WORKSPACE_ROOT and not root.startswith(os.path.abspath(WORKSPACE_ROOT)):
        return "Access outside of workspace is not allowed"
    results = []
    try:
        for r, _d, files in os.walk(root):
            for fn in files:
                fp = os.path.join(r, fn)
                try:
                    # Skip large/binary-ish files
                    if os.path.getsize(fp) > 1024 * 1024:
                        continue
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            rel = os.path.relpath(fp, WORKSPACE_ROOT or base)
                            results.append(rel)
                except Exception:
                    continue
        if not results:
            return "No matches found."
        return "\n".join(results)
    except Exception as e:
        return f"Search error: {e}"

tools = [tavily_tool, tool_read_file, tool_write_file, tool_search_workspace]
model = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo")
bound_model = model.bind_tools(tools)

async def call_model(state: AgentState):
    messages = state["messages"]
    response = await bound_model.ainvoke(messages)
    return {"messages": [response]}

async def call_tool(state: AgentState):
    last_message = state["messages"][-1]
    tool_outputs = []
    tool_by_name = {t.name: t for t in tools}
    for tool_call in getattr(last_message, "tool_calls", []) or []:
        name = tool_call.get("name") or tool_call.get("function", {}).get("name")
        args = tool_call.get("args") or tool_call.get("function", {}).get("arguments", {})
        tool = tool_by_name.get(name)
        if tool is None:
            content = f"Unknown tool: {name}"
        else:
            try:
                if hasattr(tool, "ainvoke"):
                    output = await tool.ainvoke(args)
                else:
                    output = tool.invoke(args)
                content = str(output)
            except Exception as e:
                content = f"Tool error in {name}: {e}"
        tool_outputs.append(ToolMessage(content=content, tool_call_id=tool_call["id"]))
    return {"messages": tool_outputs}

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return "end"
    return "continue"

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("action", call_tool)
graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {"continue": "action", "end": END}
)
graph.add_edge("action", "agent")
runnable = graph.compile()


# --- API DEFINITION (MODIFIED FOR MEMORY) ---

# The request now needs a conversation_id
class InvokeRequest(BaseModel):
    input: str
    conversation_id: str

async def run_graph_and_stream(user_input: str, conversation_id: str):
    """
    Runs the graph for a given conversation, maintains its state, and streams the response.
    """
    # 1. Retrieve the existing history for this conversation
    current_messages = conversation_histories[conversation_id]
    
    # 2. Add the new user message to the history
    current_messages.append(HumanMessage(content=user_input))
    
    # 3. Prepare the input for the graph
    inputs = {"messages": current_messages}
    
    final_state = None
    # 4. Use 'astream' to get real-time output
    async for output in runnable.astream(inputs, stream_mode="updates"):
        if "agent" in output:
            final_message = output["agent"]["messages"][-1]
            if final_message.content:
                response_json = {"data": final_message.content}
                yield json.dumps(response_json) + "\n"
        # Keep track of the final state of the graph
        final_state = output
    
    # 5. After the stream is complete, update the stored history
    #    with the full set of messages from the final state.
    if final_state:
        conversation_histories[conversation_id] = final_state["agent"]["messages"]


# The main endpoint, now uses the new request model
@app.post("/invoke")
async def invoke_agent(request: InvokeRequest):
    return StreamingResponse(
        run_graph_and_stream(request.input, request.conversation_id), 
        media_type="application/x-ndjson"
    )

# A new endpoint to clear the history for a conversation
class ClearRequest(BaseModel):
    conversation_id: str

@app.post("/clear_history")
async def clear_history(request: ClearRequest):
    conversation_id = request.conversation_id
    if conversation_id and conversation_id in conversation_histories:
        del conversation_histories[conversation_id]
        return JSONResponse(content={"status": "cleared", "conversation_id": conversation_id})
    return JSONResponse(content={"status": "not found"}, status_code=404)

# --- FILE SYSTEM TOOLS ---
class FileOpRequest(BaseModel):
    path: str

class FileWriteRequest(FileOpRequest):
    content: str

def _resolve_path(rel_path: str) -> str:
    base = WORKSPACE_ROOT or os.getcwd()
    abs_path = os.path.abspath(os.path.join(base, rel_path))
    # Prevent escaping workspace
    if WORKSPACE_ROOT and not abs_path.startswith(os.path.abspath(WORKSPACE_ROOT)):
        raise ValueError("Access outside of workspace is not allowed")
    return abs_path

@app.post("/fs/read")
async def fs_read(req: FileOpRequest):
    try:
        abs_path = _resolve_path(req.path)
        if not os.path.exists(abs_path):
            return JSONResponse(content={"ok": False, "error": "File not found"}, status_code=404)
        with open(abs_path, "r", encoding="utf-8") as f:
            return {"ok": True, "content": f.read()}
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e)}, status_code=400)

@app.post("/fs/write")
async def fs_write(req: FileWriteRequest):
    try:
        abs_path = _resolve_path(req.path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"ok": True}
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e)}, status_code=400)

@app.post("/fs/search")
async def fs_search(req: FileOpRequest):
    try:
        base = _resolve_path(req.path or ".")
        results = []
        for root, _dirs, files in os.walk(base):
            for fn in files:
                fp = os.path.join(root, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        results.append({"path": os.path.relpath(fp, WORKSPACE_ROOT or base), "content": content})
                except Exception:
                    continue
        return {"ok": True, "results": results}
    except Exception as e:
        return JSONResponse(content={"ok": False, "error": str(e)}, status_code=400)


# --- SERVER EXECUTION ---
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)