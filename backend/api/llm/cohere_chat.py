from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import cohere

router = APIRouter()

class ChatRequest(BaseModel):
    messages: list  # [{ role: 'user' | 'assistant' | 'system', content: str }]

@router.post("/cohere/chat")
async def cohere_chat(req: ChatRequest):
    print("chat message: ",req.messages)
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise HTTPException(status_code=500, detail=" COHERE_API_KEY not found in environment variables")

    co = cohere.Client(cohere_api_key)

    try:
        # Split out user message and prior chat history
        all_msgs = req.messages
        user_msg = all_msgs[-1]["content"]
        print("user_msg: ",user_msg)
        system_msg = all_msgs[0]["content"]
        print("system_msg: ",system_msg)

        chat_history = [
            {
                "role": "USER" if m["role"] == "user" else "CHATBOT",
                "message": m["content"]
            }
            for m in all_msgs[:-1]
            if m["role"] in ("user", "assistant") and m.get("content")
        ]
        # print("chat_history: ",chat_history)

        response = co.chat(
            model="command-r",
            temperature=0.3,
            preamble=system_msg,
            message=user_msg,
            chat_history=chat_history,
        )

        return JSONResponse(content={
            "success": True,
            "content": [{"text": response.text.strip()}]
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "content": [{"text": "Internal error talking to Cohere."}]
            }
        )
