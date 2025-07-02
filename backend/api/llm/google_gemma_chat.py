from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from google import genai # do pip install -q -U google-genai before running backend
from google.genai import types

load_dotenv()

googleAPI = os.getenv("GOOGLE_API_KEY")
if not googleAPI:
    raise HTTPException(status_code=500, detail="Google API key not configured")

client = genai.Client()
if not client:
    raise HTTPException(status_code=500, detail="Google client not configured")


router = APIRouter()

class ChatRequest(BaseModel):
    messages: list

@router.post("/google/chat")
async def get_google_gemma_chat(req: ChatRequest):

    all_msgs = req.messages
    # print("all_msgs: ",all_msgs)
    user_msg = all_msgs[-1]["content"]
    # print("user_msg: ",user_msg)
    system_msg = all_msgs[0]["content"]
    # print("system_msg: ",system_msg)

    chat_history = [
        {
            "role": "USER" if m["role"] == "user" else "CHATBOT",
            "message": m["content"]
        }
        for m in all_msgs[:-1]
        if m["role"] in ("user", "assistant") and m.get("content")
    ]
    # print("chat_history: ",chat_history)
    
    
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents= system_msg+"\n\n"+user_msg+"\n\n"+str(chat_history)+"\n\nIMPORTANT: Respond in plain text only, no markdown formatting."
    )
    # print("response: ",response.text)

    return JSONResponse(content={
            "success": True,
            "content": [{"text": response.text.strip()}]
        })


