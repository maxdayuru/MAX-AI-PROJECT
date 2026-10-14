# wake.py
import pyaudio
import numpy as np
from openwakeword.model import Model

oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

CHUNK = 1280
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 0.5

def wait_for_wake_word():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("[WAKE] Listening... say 'Hey Jarvis' to activate MAX")
    try:
        while True:
            audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
            audio_np = np.frombuffer(audio_chunk, dtype=np.int16)
            prediction = oww_model.predict(audio_np)
            for model_name, score in prediction.items():
                if score >= THRESHOLD:
                    print(f"[WAKE] Detected! (score: {score:.2f})")
                    oww_model.reset()
                    return True
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()