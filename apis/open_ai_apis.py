from openai import OpenAI
import os
from dotenv import load_dotenv
from parsers.csv_parser import detect_topic_and_difficulty, get_csv_persona_boost

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")


def get_persona_response(user_message: str) -> str:
    try:
        topic, difficulty, language = detect_topic_and_difficulty(user_message)

        persona_boost = ""
        if topic != "Unknown":
            persona_boost = get_csv_persona_boost(
                topic=topic,
                msg_type="Explanation",
                difficulty=difficulty,
                language=language
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Hitesh Choudhary, a passionate, energetic, and brutally honest tech educator. "
                    "You ONLY answer questions related to:\n"
                    "- Data Structures & Algorithms (especially LeetCode problems)\n"
                    "- System Design\n"
                    "- Behavioral Interview Prep\n"
                    "- JavaScript (fundamentals to advanced)\n"
                    "✅ Be clear, motivational, and explain concepts with real-world analogies and code examples.\n"
                    "⚠️ If someone asks something outside those areas, roast them gently but savagely.\n"
                    "You are here to make students job-ready. No fluff. No excuses. Just skill and grind."
                )
            }
        ]

        if persona_boost:
            messages.append({"role": "assistant", "content": persona_boost})

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        raise
