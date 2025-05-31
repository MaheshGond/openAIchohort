from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from twilio_webhooks.webhook import router as webhook_router
from dotenv import load_dotenv
from twilio_webhooks.webhook import router as whatsapp_webhook
from fastapi import HTTPException

# Import the Pydantic model
from pydantic import BaseModel
from apis.open_ai_apis import get_persona_response

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.include_router(whatsapp_webhook)

app = FastAPI()

app.include_router(webhook_router)

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


class ChatRequest(BaseModel):
    message: str


# POST /chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Use a dummy session id for testing
        reply = get_persona_response(request.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
