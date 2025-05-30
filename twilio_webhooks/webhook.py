from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.rest import Client as TwilioClient
import os
from dotenv import load_dotenv
from apis.open_ai_apis import get_persona_response, generate_hitesh_intro,get_persona_system_prompt

router = APIRouter()
load_dotenv()

# In-memory session tracking
session_store = {}

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    user_id = From
    twilio_client = TwilioClient(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    # First-time message
    if user_id not in session_store:
        print("User already found")
        intro = generate_hitesh_intro("Bhai")
        session_store[user_id] = [  # Store chat history
            {"role": "system", "content": get_persona_system_prompt()},
            {"role": "assistant", "content": intro},
        ]
        user_input = Body
    else:
        user_input = Body

    session_store[user_id].append({"role": "user", "content": user_input})

    last_user_message = None
    for msg in reversed(session_store[user_id]):
        if msg['role'] == 'user':
            last_user_message = msg['content']
            break
    response_text = get_persona_response(last_user_message)

    # Append bot reply
    session_store[user_id].append({"role": "assistant", "content": response_text})

    # Send WhatsApp reply
    twilio_client.messages.create(
        body=response_text[:1500],  # To stay under Twilio's 1600 char limit
        from_="whatsapp:" + os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=From
    )

    return PlainTextResponse("OK", status_code=200)
