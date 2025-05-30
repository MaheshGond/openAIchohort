# routes/webhook.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.rest import Client as TwilioClient
import os
from dotenv import load_dotenv
from apis.open_ai_apis import get_persona_response  # import your AI response logic

router = APIRouter()

load_dotenv()

@router.post("/webhook")
async def whatsapp_webhook(
        request: Request,
        Body: str = Form(...),
        From: str = Form(...)
):
    response_text = get_persona_response(Body)

    twilio_client = TwilioClient(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    twilio_client.messages.create(
        body=response_text,
        from_="whatsapp:" + os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=From
    )

    return PlainTextResponse("OK", status_code=200)
