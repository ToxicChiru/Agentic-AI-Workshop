
from langchain_core.messages import HumanMessage, ToolMessage

from agent import agent


print("=" * 60)
print("             AGENTIC RESEARCH ASSISTANT")
print("=" * 60)

question = input("\nEnter your research question: ")

try:

    # Send the question to the LangGraph agent
    result = agent.invoke({
        "messages": [
            HumanMessage(content=question)
        ]
    })

    # Display the execution trace
    print("\n" + "=" * 60)
    print("                 EXECUTION TRACE")
    print("=" * 60)

    for message in result["messages"]:

        # Display tool selection
        if getattr(message, "tool_calls", None):

            for call in message.tool_calls:
                print("\nTool selected:", call["name"])
                print("Arguments:", call["args"])

        # Display tool output
        if isinstance(message, ToolMessage):
            print("Tool output:", message.content)

    # Display the final response
    print("\n" + "=" * 60)
    print("                 FINAL RESPONSE")
    print("=" * 60)

    final_message = result["messages"][-1]

    print(final_message.content)

except Exception as e:
    print("\nApplication error:", e)
