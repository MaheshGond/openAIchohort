from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from twilio_webhooks.webhook import router as whatsapp_webhook
# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.include_router(whatsapp_webhook)

# Enable CORS (optional but useful if frontend is separate)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test route
@app.get("/")
def read_root():
    return {"message": "Hitesh Choudhary Persona Bot Backend is running"}


from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# Import the Pydantic model
from pydantic import BaseModel
from apis.open_ai_apis import get_persona_response


class ChatRequest(BaseModel):
    message: str

from fastapi import FastAPI
from twilio_webhooks.webhook import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)

# POST /chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Use a dummy session id for testing
        reply = get_persona_response(request.message, user_id="test-user")
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
