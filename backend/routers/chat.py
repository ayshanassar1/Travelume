from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional

from modules.travel_coach import travel_coach
from backend.routers.auth import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

class MessageRequest(BaseModel):

    session_id: str
    text: str

class ChatResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None
    is_completed: bool = False
    session_id: Optional[str] = None

@router.post("/start", response_model=ChatResponse)
async def start_chat_session(current_user: dict = Depends(get_current_user)):
    try:
        user_email = current_user["email"]
        result = travel_coach.start_session(user_email)
        return ChatResponse(
            session_id=result["session_id"],
            text=result["text"],
            audio_url=result["audio_url"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=ChatResponse)
async def send_message(
    session_id: str = Form(...),
    text: str = Form(...),
    file: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Security: Verify session ownership
        session = travel_coach._load_session(session_id)
        if not session or session.get("user_email") != current_user["email"]:
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this session")

        # Read file if present
        file_data = None
        if file:
            file_data = {
                "filename": file.filename,
                "content_type": file.content_type,
                "bytes": await file.read()
            }
            
        result = travel_coach.process_message(session_id, text, file_data)

        return ChatResponse(
            text=result["text"],
            audio_url=result["audio_url"],
            is_completed=result.get("is_completed", False)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
