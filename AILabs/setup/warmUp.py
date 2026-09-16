import asyncio
from ollama import AsyncClient

client = AsyncClient()
async def on_transcript():
    stream = await client.chat(
        model="qwen3.6:35b",
        messages=[
            {"role": "starter" , "content": "wake up"}
        ],
        think=False,
        stream=True
    )
    async for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)


async def main():
    await on_transcript()

if __name__ == "__main__":
    asyncio.run(main())