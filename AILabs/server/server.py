import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from elevenlabs import AsyncElevenLabs

load_dotenv()

# Replace with your Speech Engine ID from step 4
SPEECH_ENGINE_ID = "seng_4901m2k517adf2xst4acyfc3g79r"

openai = AsyncOpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)
elevenlabs = AsyncElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)


def on_init(conversation_id, session):
    print(f"Session started: {conversation_id}")


async def on_transcript(transcript, session):
    stream = await openai.responses.create(
        model="gpt-4o",
        instructions="You are a helpful voice assistant. Keep responses concise and conversational.",
        input=[
            {"role": "assistant" if m.role == "agent" else m.role, "content": m.content}
            for m in transcript
        ],
        stream=True,
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
        path="/ws",
        debug=True,
        on_init=on_init,
        on_transcript=on_transcript,
        on_close=on_close,
        on_error=on_error,
    )


if __name__ == "__main__":
    asyncio.run(main())
