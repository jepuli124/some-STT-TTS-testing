from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

def SpeechToText(filePath):

    with open(filePath, "rb") as audioFile:
        # Load variables from .env file into os.environ
        load_dotenv()

        client = ElevenLabs(
            api_key=os.getenv('ELEVENLABS_API_KEY')
        )

        file = audioFile.read()

        transcription = client.speech_to_text.convert(
            file=file,
            model_id="scribe_v2", # Model to use
            tag_audio_events=True, # Tag audio events like laughter, applause, etc.
            #language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
            diarize=True, # Whether to annotate who is speaking
        )
        return(transcription.text)
