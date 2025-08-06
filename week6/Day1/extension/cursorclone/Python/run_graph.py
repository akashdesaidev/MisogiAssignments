import os
import sys
import json
import asyncio
from typing import TypedDict, Annotated

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# --- SETUP ---
# Load environment variables from a .env file
load_dotenv()

# Define the FastAPI app
app = FastAPI()

# --- LANGGRAPH LOGIC (Copied from your old script) ---

# 1. Define the State
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]

# 2. Define the Tools
tavily_tool = TavilySearch(max_results=3)
tools = [tavily_tool]

# 3. Define the Model
model = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo")
bound_model = model.bind_tools(tools)

# 4. Define the Graph Nodes
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
    if not last_message.tool_calls:
        return "end"
    return "continue"

# 5. Construct the Graph
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


# --- API DEFINITION ---

# Define the request body model for type checking
class InvokeRequest(BaseModel):
    input: str

async def run_graph_and_stream(user_input: str):
    """A generator function that runs the graph and yields the final results."""
    inputs = {"messages": [HumanMessage(content=user_input)]}
    
    # Use 'astream' to get real-time output from the graph
    async for output in runnable.astream(inputs):
        if "agent" in output:
            final_message = output["agent"]["messages"][-1]
            if final_message.content:
                # Yield the content in the JSON format the client expects
                response_json = {"data": final_message.content}
                yield json.dumps(response_json) + "\n"

# Define the API endpoint
@app.post("/invoke")
async def invoke_agent(request: InvokeRequest):
    """
    This endpoint receives a user's message, runs the agent,
    and streams the response back.
    """
    return StreamingResponse(run_graph_and_stream(request.input), media_type="application/x-ndjson")

# --- SERVER EXECUTION ---
if __name__ == "__main__":
    # Runs the server on localhost, port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)