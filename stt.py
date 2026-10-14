# stt.py
# stt.py
import whisper
import pyaudio
import numpy as np
import soundfile as sf
import tempfile
import os

model = whisper.load_model("tiny.en")

SAMPLE_RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 500
SILENCE_SECONDS = 1.5
MAX_SECONDS = 10

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=SAMPLE_RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("[STT] Recording... (speak now)")

    frames = []
    silent_chunks = 0
    speaking_started = False
    max_chunks = int(SAMPLE_RATE / CHUNK * MAX_SECONDS)
    silence_limit = int(SAMPLE_RATE / CHUNK * SILENCE_SECONDS)

    for _ in range(max_chunks):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        audio_np = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_np).mean()

        if volume > SILENCE_THRESHOLD:
            speaking_started = True
            silent_chunks = 0
        elif speaking_started:
            silent_chunks += 1
            if silent_chunks >= silence_limit:
                print("[STT] Silence detected, processing...")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_np = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio_float = audio_np.astype(np.float32) / 32768.0

    tmp = tempfile.NamedTemporaryFile(suffix=".flac", delete=False)
    sf.write(tmp.name, audio_float, SAMPLE_RATE)
    return tmp.name

def transcribe(audio_path):
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=False,
        condition_on_previous_text=False,
        temperature=0,
    )
    os.unlink(audio_path)
    text = result["text"].strip()
    print(f"[STT] Heard: {text}")
    return text

def listen_and_transcribe(duration=None):
    path = record_audio()
    return transcribe(path)# stt.py
import whisper
import pyaudio
import numpy as np

model = whisper.load_model("tiny.en")

SAMPLE_RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 500
SILENCE_SECONDS = 1.5
MAX_SECONDS = 10

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=SAMPLE_RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("[STT] Recording... (speak now)")

    frames = []
    silent_chunks = 0
    speaking_started = False
    max_chunks = int(SAMPLE_RATE / CHUNK * MAX_SECONDS)
    silence_limit = int(SAMPLE_RATE / CHUNK * SILENCE_SECONDS)

    for _ in range(max_chunks):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        audio_np = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_np).mean()

        if volume > SILENCE_THRESHOLD:
            speaking_started = True
            silent_chunks = 0
        elif speaking_started:
            silent_chunks += 1
            if silent_chunks >= silence_limit:
                print("[STT] Silence detected, processing...")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert to float32 numpy array — pass directly to Whisper, no file needed
    audio_np = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio_float = audio_np.astype(np.float32) / 32768.0
    return audio_float

def transcribe(audio_float):
    # Pass numpy array directly — completely bypasses ffmpeg
    result = model.transcribe(
        audio_float,
        language="en",
        fp16=False,
        condition_on_previous_text=False,
        temperature=0,
    )
    text = result["text"].strip()
    print(f"[STT] Heard: {text}")
    return text

def listen_and_transcribe(duration=None):
    audio = record_audio()
    return transcribe(audio)