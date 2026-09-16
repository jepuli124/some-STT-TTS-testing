import wave, winsound
from piper import PiperVoice

# from threading import Thread

voice = PiperVoice.load("./voices/en_US-amy-medium.onnx")

def speak(text):
    with wave.open("speak.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    winsound.PlaySound("speak.wav", winsound.SND_FILENAME)

 
# simpleaudio module caused problems (shutdown the server once I was done) that I tried to fix with threading.
# def speakStart(text):
#     threadObject = Thread(target=speak, args=[text])
#     threadObject.start()
    