CRISIS_KEYWORDS = [
    "suicide",
    "kill myself",
    "end my life",
    "worthless",
    "hopeless",
    "can't go on"
]

def detect_crisis(message: str) -> bool:
    msg = message.lower()
    return any(word in msg for word in CRISIS_KEYWORDS)


def generate_cbt_response(message: str) -> str:
    return (
        "I'm really glad you reached out. It sounds like you're going through a lot right now. "
        "Try taking a slow deep breath with me. You're not alone, and support is available."
    )


def run_mental_health_agent(message: str) -> dict:
    crisis = detect_crisis(message)

    if crisis:
        return {
            "risk": "high",
            "response": (
                "I'm really concerned about your safety. "
                "Please reach out to a trusted person or a mental health professional immediately. "
                "If you are in danger, contact your local emergency services right now."
            ),
            "escalation": True
        }

    return {
        "risk": "low",
        "response": generate_cbt_response(message),
        "escalation": False
    }
