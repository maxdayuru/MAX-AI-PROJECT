# main.py
import threading
import webbrowser
import time
import app as flask_app
from wake import wait_for_wake_word
from stt import listen_and_transcribe
from memory import recall_memory, save_memory
from brain import think
from emotion import detect_emotion, get_tone_hint
from tts_engine import speak

def run_flask():
    flask_app.app.run(port=5000, debug=False, use_reloader=False)

def main():
    print("\n=== MAX AI is starting ===\n")

    # Start Flask UI in background
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    # Open browser after Flask is ready
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")
    print("[MAX] Hologram UI opened at http://127.0.0.1:5000")
    print("[MAX] Say 'Hey Jarvis' to activate\n")

    while True:
        try:
            # Step 1: Wait for wake word
            wait_for_wake_word()

            # Step 2: Record and transcribe
            flask_app.update_state("Listening...", "neutral", False)
            user_input = listen_and_transcribe()
            print(f"[USER] {user_input}")

            # Skip empty or too short input
            if not user_input or len(user_input.strip()) < 2:
                print("[MAX] Nothing heard, going back to sleep.")
                flask_app.update_state("", "neutral", False)
                continue

            # Step 3: Detect emotion
            emotion = detect_emotion(user_input)
            tone = get_tone_hint(emotion)
            print(f"[EMOTION] {emotion}")

            # Step 4: Recall memory for longer inputs only
            memory = ""
            if len(user_input.split()) > 4:
                memory = recall_memory(user_input)

            # Step 5: Generate response
            flask_app.update_state("Thinking...", emotion, False)
            print("[MAX] Thinking...")
            response = think(user_input, memory_context=memory, emotion_hint=tone)
            print(f"[MAX] {response}")

            # Step 6: Save to memory
            save_memory(user_input, response)

            # Step 7: Speak response
            flask_app.update_state(response, emotion, True)
            speak(response)
            flask_app.update_state("", "neutral", False)

        except KeyboardInterrupt:
            print("\n[MAX] Shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"[MAX] Error in main loop: {e}")
            flask_app.update_state("", "neutral", False)
            continue

if __name__ == "__main__":
    main()