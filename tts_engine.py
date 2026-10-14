# tts_engine.py
import pyttsx3
import threading
import re

def _clean_for_speech(text: str) -> str:
    # Remove anything that sounds weird when spoken
    text = re.sub(r'http\S+', 'a web link', text)
    text = re.sub(r'[*#`_~]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def speak(text: str):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 185)
            engine.setProperty('volume', 1.0)
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            clean = _clean_for_speech(text)
            print(f"[TTS] Speaking: {clean[:80]}...")
            engine.say(clean)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"[TTS] Error: {e}")
    t = threading.Thread(target=_speak, daemon=True)
    t.start()
    t.join()