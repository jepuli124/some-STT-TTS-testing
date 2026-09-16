import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

# Offline TTS using pyttsx3
def text_to_speech_offline(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Offline STT using Vosk
def speech_to_text_offline():
    model = Model("./models/vosk-model-small-en-us-0.15/", "model-fi")  # Replace with the path to your Finnish Vosk model
    recognizer = KaldiRecognizer(model, 16000)

    print("Puhukaa nyt...")  # Speak now
    with sd.RawInputStream(samplerate=16000, channels=1, dtype='int16') as stream:
        while True:
            data = stream.read(4000)
            if recognizer.AcceptWaveform(data[0]):
                result = json.loads(recognizer.Result())
                print("Sanoit:", result.get("text"))
                return result.get("text")

# Main Program
def main():
    print("Puhukaa jotakin, ja toistan sen.")  # Speak something, and I will repeat it
    spoken_text = speech_to_text_offline()
    if spoken_text:
        text_to_speech_offline(f"Sanoit: {spoken_text}")

if __name__ == "__main__":
    main()