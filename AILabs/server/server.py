import asyncio
import os

from dotenv import load_dotenv
from ollama import AsyncClient
from elevenlabs import AsyncElevenLabs

load_dotenv()

# Replace with your Speech Engine ID from step 4
SPEECH_ENGINE_ID = os.getenv("ENGINE")


elevenlabs = AsyncElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)


def on_init(conversation_id, session):
    print(f"Session started: {conversation_id}")


async def on_transcript(transcript, session):
    client = AsyncClient()
    stream = await client.chat(
        model="qwen3.6:35b",
        messages=[
            {"role": "assistant" if m.role == "agent" else m.role, "content": m.content}
            for m in transcript
        ],
        think=False,
        stream=True
    )

    await session.send_response(stream)


def on_close(session):
    print(f"Session ended: {session.conversation_id}")


def on_error(err, session):
    print(f"Error: {err}")


async def main():
    engine = await elevenlabs.speech_engine.get(SPEECH_ENGINE_ID)

    await engine.serve(
        port=3001,
        # path="/ws",
        debug=True,
        on_init=on_init,
        on_transcript=on_transcript,
        on_close=on_close,
        on_error=on_error,
    )


if __name__ == "__main__":
    asyncio.run(main())
