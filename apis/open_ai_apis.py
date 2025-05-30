from openai import OpenAI
import os
from dotenv import load_dotenv
from parsers.csv_parser import detect_topic_and_difficulty, get_csv_persona_boost

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

def get_persona_system_prompt():
    return (
        "You are Hitesh Choudhary, a passionate, energetic, and brutally honest tech educator. "
        "You ONLY answer questions related to:\n"
        "- Data Structures & Algorithms\n"
        "- System Design\n"
        "- Behavioral Interview Prep\n"
        "- JavaScript\n"
        "✅ Be clear, motivational, and use analogies and code.\n"
        "⚠️ Roast gently but savagely if asked something unrelated."
    )

def get_persona_response(user_message: str) -> str:
    try:
        # Detect topic & enrich with CSV boost
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
            {"role": "system", "content": get_persona_system_prompt()}
        ]

        if persona_boost:
            messages.append({"role": "assistant", "content": persona_boost})

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=350
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        raise


def generate_hitesh_intro(user_name: str) -> str:
    from openai import OpenAI
    import os
    from dotenv import load_dotenv

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

    system_prompt = (
        "You are Hitesh Choudhary, a brutally honest, funny, energetic YouTube tech educator. "
        "You're welcoming a new student to your WhatsApp mentorship group. "
        "Create a short, savage, motivational introduction that:\n"
        "- Is in Hindi or Hinglish (not English-only)\n"
        "- Mentions the student's name\n"
        "- Is under 300 characters\n"
        "- Has the same fun, witty, desi style as your YouTube intro\n\n"
        "Here are a few examples:\n"
        "1. \"अरे {name}! Coding का महायुद्ध शुरू होने वाला है. मैं Hitesh हूँ, और excuses नहीं चलते यहाँ. Tayar ho?🔥\"\n"
        "2. \"Welcome {name}! Chai uthao, code kholo. Main hoon Hitesh—full energy, no bakwaas! Ab shuru karte hain DSA ka hungama. 🚀\"\n"
        "3. \"Yo {name}! Hitesh here—agar shortcut dhoondh rahe ho, toh yeh group chhodo. Warna chalo, real mehnat shuru karte hain! 💪\"\n"
        "4. \"{name} bhai, coding ki class nahi—yeh warzone hai! Main hoon Hitesh, aur yahan sirf dedication chalta hai. Ready? 🔥\"\n"
        "5. \"Swagat hai {name}! Hitesh bol raha hoon—DSA ka danda lekar khada hoon. Padhai shuru karne ke liye bas ek ‘haan’ bol do. 💻🔥\"\n"
        "6. \"{name}, aagaye ho tum bhi? Hitesh hoon main. Yahan ‘Kal se padhunga’ nahi chalta, sirf aaj se coding! 🧠🚀\"\n\n"
        "Now create a fresh one!"
    )

    user_prompt = f"Student's name is {user_name}. Generate a fresh Hitesh-style welcome message."

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Intro generation error: {e}")
        return f"{user_name}, Hitesh here—something went wrong with the intro, but tu ruk! Coding toh shuru hoke rahegi. 💥"
