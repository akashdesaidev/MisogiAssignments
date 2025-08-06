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
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
app = FastAPI()

# --- SERVER-SIDE MEMORY ---
# We use a defaultdict that creates a new list for any new conversation_id
conversation_histories = defaultdict(list)

# --- LANGGRAPH LOGIC (Unchanged) ---
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]

tavily_tool = TavilySearch(max_results=3)
tools = [tavily_tool]
model = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo")
bound_model = model.bind_tools(tools)

async def call_model(state: AgentState):
    messages = state["messages"]
    response = await bound_model.ainvoke(messages)
    return {"messages": [response]}

async def call_tool(state: AgentState):
    last_message = state["messages"][-1]
    tool_outputs = []
    for tool_call in last_message.tool_calls:
        tool = tools[0]
        output = await tool.ainvoke(tool_call["args"])
        tool_outputs.append(
            ToolMessage(content=str(output), tool_call_id=tool_call["id"])
        )
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
    async for output in runnable.astream(inputs):
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
@app.post("/clear_history")
async def clear_history(request: BaseModel): # A simple request with just a conversation_id
    conversation_id = getattr(request, 'conversation_id', None)
    if conversation_id and conversation_id in conversation_histories:
        del conversation_histories[conversation_id]
        return JSONResponse(content={"status": "cleared", "conversation_id": conversation_id})
    return JSONResponse(content={"status": "not found"}, status_code=404)


# --- SERVER EXECUTION ---
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)