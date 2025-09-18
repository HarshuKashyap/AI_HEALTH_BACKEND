from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_logic import get_answer  # KB + OpenAI dono

app = FastAPI()

# CORS allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development ke liye
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Health Assistant Running 🚀"}

class ChatRequest(BaseModel):
    message: str

# ✅ Make sure this matches your React fetch
@app.post("/chat/message")
def chat_message(req: ChatRequest):
    answer = get_answer(req.message)
    return {"answer": answer}   # key should be "answer" for React fetch

