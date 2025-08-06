const { StateGraph } = require("@langchain/langgraph");
// FIX 1: Import TavilySearchResults instead of the retriever
const {
  TavilySearchResults,
} = require("@langchain/community/tools/tavily_search");
const { ChatOpenAI } = require("@langchain/openai");

// Define the state interface
const agentState = {
  messages: {
    value: (x, y) => x.concat(y),
    default: () => [],
  },
};

// Define the tools
// FIX 2: Instantiate the correct class. You can also pass options like maxResults.
const tavilySearch = new TavilySearchResults({
  apiKey: process.env.TAVILY_API_KEY,
  k: 3,
});

const tools = [tavilySearch];

// Define the model
const model = new ChatOpenAI({
  temperature: 0,
  streaming: true,
  model: "gpt-3.5-turbo",
});

// model.bindTools is smart enough to convert the tool instance to the correct format
const boundModel = model.bindTools(tools);

// Define the graph
const graph = new StateGraph({
  channels: agentState,
});

// Define the nodes
const shouldContinue = (state) => {
  const { messages } = state;
  const lastMessage = messages[messages.length - 1];
  // Check if the model decided to call a tool
  if (
    !lastMessage ||
    !lastMessage.tool_calls ||
    lastMessage.tool_calls.length === 0
  ) {
    return "end";
  }
  return "continue";
};

const callModel = async (state) => {
  const { messages } = state;
  const response = await boundModel.invoke(messages);
  return { messages: [response] };
};

const callTool = async (state) => {
  const { messages } = state;
  const lastMessage = messages[messages.length - 1];

  // This part needs to be more robust to handle multiple tool calls
  const tool = tools.find((t) => t.name === lastMessage.tool_calls[0].name);
  // NOTE: The output of a tool should be a string for the model to process.
  // The .invoke method of TavilySearchResults already returns a string of results.
  const output = await tool.invoke(lastMessage.tool_calls[0].args);

  // The LangChain AI Message type for tool results is now preferred
  const { ToolMessage } = require("@langchain/core/messages");
  const toolMessage = new ToolMessage({
    content: output,
    tool_call_id: lastMessage.tool_calls[0].id,
  });

  return { messages: [toolMessage] };
};

// Add the nodes to the graph
graph.addNode("agent", callModel);
graph.addNode("action", callTool);

// Set the entry point
graph.setEntryPoint("agent");

// Add the conditional edges
graph.addConditionalEdges("agent", shouldContinue, {
  continue: "action",
  end: "__end__", // Use the official end node
});

// Add the normal edge
graph.addEdge("action", "agent");

// Compile the graph
const runnable = graph.compile();

module.exports = runnable;
