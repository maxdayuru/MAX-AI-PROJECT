# emotion.py

EMOTION_KEYWORDS = {
    "happy":   ["great", "awesome", "love", "happy", "excited", "yay", "wonderful", "amazing", "fantastic", "good"],
    "sad":     ["sad", "depressed", "down", "unhappy", "cry", "miss", "lonely", "upset", "hurt", "terrible"],
    "angry":   ["angry", "frustrated", "annoyed", "hate", "mad", "furious", "stupid", "useless", "worst"],
    "curious": ["how", "why", "what", "explain", "curious", "wonder", "tell me", "describe", "difference", "meaning"],
    "neutral": []
}

TONE_HINTS = {
    "happy":   "Be enthusiastic, warm, and upbeat.",
    "sad":     "Be gentle, empathetic, and comforting.",
    "angry":   "Be calm, patient, and understanding.",
    "curious": "Be clear, informative, and engaging. Give a thorough explanation.",
    "neutral": "Be natural, friendly, and conversational."
}

def detect_emotion(text: str) -> str:
    text_lower = text.lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return emotion
    return "neutral"

def get_tone_hint(emotion: str) -> str:
    return TONE_HINTS.get(emotion, "Be natural and conversational.")