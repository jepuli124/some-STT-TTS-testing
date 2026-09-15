
import ollama

stream = ollama.chat(
        model="qwen3.6:35b",
        messages=[
            {"role": "user", "content": "Hello there, how are you?"}
        ]
    )

print(stream)