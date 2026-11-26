
from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from tools import TOOLS


# 1. Connect to the local LLM
llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

# 2. Give the LLM access to our tools
llm_with_tools = llm.bind_tools(TOOLS)


# 3. Define the agent node
def agent_node(state: MessagesState):

    system_message = {
        "role": "system",
        "content": """
        You are a helpful research assistant.

        You have access to three tools:
        1. Calculator
        2. Dataset search
        3. Information retrieval

        Use the appropriate tools whenever the question
        requires numerical calculations or information
        from the local research dataset.

        You may call more than one tool when necessary.

        After receiving tool results, evaluate whether
        further tool calls are needed.

        For dataset searches, report the exact matching record count,
        total dataset record count, and relevant topics from the tool result.
        Do not estimate counts or invent topics.

        Provide a detailed and clear final response.
        Do not invent information from the dataset.
        """
    }

    messages = [system_message] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


# 4. Create the graph
builder = StateGraph(MessagesState)

# Add nodes
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))

# Define the execution flow
builder.add_edge(START, "agent")

# Route according to the LLM's tool-call decision
builder.add_conditional_edges(
    "agent",
    tools_condition
)

# Return tool results to the agent
builder.add_edge("tools", "agent")

# Compile the graph
agent = builder.compile()
