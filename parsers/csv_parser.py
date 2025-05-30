import re
from parsers.csv_reader import return_messges_df
import random


def get_csv_persona_boost(topic: str, msg_type: str, difficulty: str, language: str = "Bilingual") -> str:
    messages_df = return_messges_df()
    filtered = messages_df[
        (messages_df["Topic"].str.lower() == topic.lower()) &
        (messages_df["Difficulty"].str.lower() == difficulty.lower()) &
        (messages_df["Language"].str.lower() == language.lower())
        ]
    if filtered.empty:
        return ""
    return random.choice(filtered["Message"].tolist())


def detect_topic_and_difficulty(message: str):
    message = message.lower()

    # Topic Detection
    if any(kw in message for kw in ["recursion", "tree", "array", "linked list", "graph", "sliding window"]):
        topic = "DSA"
    elif any(kw in message for kw in ["load balancer", "cache", "database", "api gateway", "scaling"]):
        topic = "System Design"
    elif any(kw in message for kw in ["closure", "promise", "async", "hoisting", "dom", "event loop", "javascript"]):
        topic = "JavaScript"
    elif any(kw in message for kw in ["interview", "strength", "weakness", "tell me about yourself"]):
        topic = "Behavioral"
    else:
        topic = "Unknown"

    # Difficulty Detection
    if any(kw in message for kw in ["easy", "beginner", "first time", "just started"]):
        difficulty = "Beginner"
    elif any(kw in message for kw in ["medium", "average", "not too hard"]):
        difficulty = "Intermediate"
    elif any(kw in message for kw in ["hard", "difficult", "advanced", "complex", "hardcore"]):
        difficulty = "Advanced"
    else:
        difficulty = "Intermediate"  # Default fallback

    # Language Detection
    if re.search(r'[अ-ह]+', message):
        language = "Hindi"
    elif any(kw in message for kw in ["hindi", "english", "bilingual"]):
        if "hindi" in message:
            language = "Hindi"
        elif "english" in message:
            language = "English"
        else:
            language = "Bilingual"
    else:
        language = "Bilingual"

    return topic, difficulty, language
