import whisper
import pyttsx3
import sounddevice as sd
import numpy as np

class Voice:

    def __init__(self):
        
        self.engine = pyttsx3.init()
    
    def speak(self,text):
        
        self.engine.setProperty('rate', 150)  
        self.engine.say(text)
        self.engine.runAndWait()

class Hear:
    def __init__(self):
        self.model = whisper.load_model("base").to("cuda")

    def record_audio(self, duration=20, samplerate=16000):
        print("Hearing...")
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
        sd.wait()  
        print("Processing...")
        return audio.flatten()

    def hear(self):
        audio = self.record_audio()
        result = self.model.transcribe(audio)
        return result["text"]
    

