
import ollama
import json

from tools import (
    calculator,
    search_dataset,
    retrieve_information
)

print("=" * 55)
print("          AGENTIC RESEARCH ASSISTANT")
print("=" * 55)

question = input("\nEnter your question: ")

# Define the available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform numerical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["sum", "average", "maximum", "minimum"]
                    },
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"}
                    }
                },
                "required": ["operation", "numbers"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_dataset",
            "description": "Search the local research CSV dataset using a keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword to search for"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_information",
            "description": "Retrieve the complete dataset record for a specific research topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Name of the research topic"
                    }
                },
                "required": ["topic"]
            }
        }
    }
]

messages = [
    {
        "role": "system",
        "content": """
        You are a research assistant.

        You have access to three tools:
        1. Calculator
        2. Dataset search
        3. Information retrieval

        Select an appropriate tool whenever the user's
        question requires calculations or information
        from the local research dataset.

        Use the returned tool results to formulate
        a clear and detailed final response.

        Do not invent dataset records.
        """
    },
    {
        "role": "user",
        "content": question
    }
]

# Tool execution
try:

    response = ollama.chat(
        model="qwen3:4b",
        messages=messages,
        tools=tools
    )

    tool_calls = response["message"].get("tool_calls", [])

    if tool_calls:

        # Add the assistant's tool-call message to history
        messages.append(response["message"])

        for tool_call in tool_calls:

            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            print("\nTool selected:", function_name)
            print("Tool arguments:", arguments)

            # Execute the selected Python function
            if function_name == "calculator":
                result = calculator(
                    arguments["operation"],
                    arguments["numbers"]
                )

            elif function_name == "search_dataset":
                result = search_dataset(
                    arguments["query"]
                )

            elif function_name == "retrieve_information":
                result = retrieve_information(
                    arguments["topic"]
                )

            else:
                result = "Unknown tool requested."

            print("Tool result:", result)

            # Return the result to the LLM
            messages.append({
                "role": "tool",
                "tool_name": function_name,
                "content": json.dumps(result, default=str)
            })

        # Generate final response using tool results
        final_response = ollama.chat(
            model="qwen3:4b",
            messages=messages
        )

        print("\nAssistant:")
        print(final_response["message"]["content"])

    else:

        print("\nAssistant:")
        print(response["message"]["content"])

except Exception as e:
    print("\nError:", e)
