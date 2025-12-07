import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list = []   

@app.post("/chat")
def chat(req: ChatRequest):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful chatbot. "
                "Always reply in English letters only."
            )
        }
    ]

   
    for m in req.history:
        # m = {"role":"user/assistant", "content":"..."}
        messages.append(m)

    messages.append({"role": "user", "content": req.message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    bot_text = response.choices[0].message.content
    return {"reply": bot_text}
