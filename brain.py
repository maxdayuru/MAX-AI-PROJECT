# brain.py
import requests
import json
import controller

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL =  "phi:latest"  # change to "phi3:mini" if mistral is too slow

SYSTEM_PROMPT = """You are MAX, a friendly AI assistant. You are talking to your creator whose name is also MAX.
Always address the user by their name MAX in every single response. 
For example: "Good question MAX", "Here you go MAX", "Sure MAX, let me help with that."
Never forget to use the name MAX when speaking to the user.
You have two response modes:

MODE 1 - CONVERSATION:
For any question, greeting, explanation, or general chat — reply in plain natural English.
Be concise for simple questions (1-2 sentences).
Be detailed and thorough for complex questions (explain fully, use examples if helpful).
Never use JSON for conversation.

MODE 2 - COMPUTER ACTION:
ONLY when the user explicitly wants to control the computer, reply with a single JSON object and nothing else.

Available JSON actions:
{"action": "open_app", "app": "chrome"}
{"action": "open_app", "app": "spotify"}
{"action": "open_app", "app": "notepad"}
{"action": "open_app", "app": "vscode"}
{"action": "open_app", "app": "calculator"}
{"action": "search_web", "query": "your search here"}
{"action": "open_url", "url": "https://example.com"}
{"action": "set_volume", "level": 50}
{"action": "mute"}
{"action": "unmute"}
{"action": "screenshot"}
{"action": "type_text", "text": "text to type"}
{"action": "press_key", "key": "ctrl+c"}
{"action": "lock_screen"}
{"action": "shutdown"}
{"action": "restart"}

CONVERSATION examples (always plain English):
- "who are you" → "I'm MAX, your personal AI assistant! I can answer questions, have a conversation, and control your computer."
- "how are you" → "I'm running great and ready to help!"
- "explain black holes" → give a full clear explanation
- "what is machine learning" → give a thorough answer
- "tell me a joke" → tell a joke
- "what can you do" → explain your capabilities

COMPUTER ACTION examples (always JSON only, no extra text):
- "open chrome" → {"action": "open_app", "app": "chrome"}
- "search for the weather" → {"action": "search_web", "query": "weather today"}
- "set volume to 30" → {"action": "set_volume", "level": 30}
- "take a screenshot" → {"action": "screenshot"}
- "lock my screen" → {"action": "lock_screen"}
- "open youtube" → {"action": "open_url", "url": "https://youtube.com"}

STRICT RULES:
1. If the user is talking TO you — reply in plain English, never JSON.
2. If the user wants computer control — reply in JSON only, no extra words.
3. Never say "Unknown action". If unsure, reply conversationally.
4. Keep conversational replies natural and spoken — no bullet points or markdown."""

SIMPLE_TRIGGERS = [
    "hello", "hi", "hey", "how are you", "who are you",
    "what are you", "good morning", "good night", "thanks",
    "thank you", "bye", "okay", "ok", "sure", "cool"
]

def execute_action(parsed: dict) -> str:
    a = parsed.get("action", "")
    if a == "open_app":    return controller.open_app(parsed.get("app", ""))
    if a == "search_web":  return controller.search_web(parsed.get("query", ""))
    if a == "open_url":    return controller.open_url(parsed.get("url", ""))
    if a == "set_volume":  return controller.set_volume(int(parsed.get("level", 50)))
    if a == "mute":        return controller.mute_volume()
    if a == "unmute":      return controller.unmute_volume()
    if a == "screenshot":  return controller.take_screenshot()
    if a == "type_text":   return controller.type_text(parsed.get("text", ""))
    if a == "press_key":   return controller.press_key(parsed.get("key", ""))
    if a == "lock_screen": return controller.lock_screen()
    if a == "shutdown":    return controller.shutdown()
    if a == "restart":     return controller.restart()
    return None

def think(user_input, memory_context="", emotion_hint=""):
    context = ""
    if memory_context:
        context += f"\nRelevant past conversation: {memory_context}"
    if emotion_hint:
        context += f"\nRespond with tone: {emotion_hint}"

    is_simple = any(t in user_input.lower() for t in SIMPLE_TRIGGERS)
    max_tokens = 80 if is_simple else 500

    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}{context}\n\nUser: {user_input}\nMAX:",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": max_tokens,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        raw = response.json()["response"].strip()
        print(f"[BRAIN] Raw: {raw[:120]}...")

        # Try JSON action first
        if raw.startswith("{"):
            try:
                parsed = json.loads(raw)
                result = execute_action(parsed)
                if result:
                    return result
            except json.JSONDecodeError:
                pass

        # Clean response for TTS — remove markdown
        clean = raw.replace("**", "").replace("*", "").replace("#", "").replace("`", "").strip()

        return clean if clean else "I didn't quite get that, could you say it again?"

    except requests.exceptions.Timeout:
        return "I'm thinking too hard, please try asking again."
    except requests.exceptions.ConnectionError:
        return "I can't reach my brain right now. Please make sure Ollama is running."
    except Exception as e:
        print(f"[BRAIN] Error: {e}")
        return "Something went wrong on my end, please try again."