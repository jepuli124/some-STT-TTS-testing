from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from dotenv import load_dotenv
import os


# Load variables from .env file into os.environ
load_dotenv()

client = ElevenLabs(
    api_key=os.getenv('ELEVENLABS_API_KEY')
)

def TextToSpeech(text):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="hpp4J3VqNfWAUOO0d1Us",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    return play(audio)