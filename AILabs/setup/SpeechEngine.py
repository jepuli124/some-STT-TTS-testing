
import asyncio, os
from dotenv import load_dotenv
from elevenlabs import AsyncElevenLabs

load_dotenv()

elevenlabs = AsyncElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)


async def main():
    engine = await elevenlabs.speech_engine.create(
        name="My Speech Engine",
        speech_engine={
            # Note we use the wss protocol instead of https
            "ws_url": "wss://saloon-sharper-attach.ngrok-free.dev",
        },
    )

    print(f"Speech Engine ID: {engine.engine_id}")


if __name__ == "__main__":
    asyncio.run(main())
