
import ollama

print("=" * 50)
print("       AGENTIC RESEARCH ASSISTANT")
print("=" * 50)

question = input("\nEnter your research question: ")

print("\nAssistant: ", end="", flush=True)

try:
    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a knowledgeable research assistant. "
                    "Provide detailed, technically accurate and "
                    "well-structured answers. Explain concepts "
                    "with relevant examples wherever appropriate."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        stream=True
    )

    for chunk in response:
        message = chunk["message"]

        if message.get("content"):
            print(message["content"], end="", flush=True)

    print("\n\nResponse completed.")

except Exception as e:
    print("\nError:", e)
