from fastapi import APIRouter, HTTPException, Depends
from typing import List
import os
from datetime import datetime

# Import Database and Models
from modules.database import get_database
from backend.models import Journal
from backend.routers.auth import get_current_user

router = APIRouter(
    prefix="/journals",
    tags=["Journals"]
)


@router.get("/")
async def get_journals(current_user: dict = Depends(get_current_user)):
    user_email = current_user["email"]
    db = get_database()
    try:
        return db.get_user_journals(user_email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{journal_id}")
async def get_journal(journal_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        journal = db.get_journal(journal_id)
        if not journal:
            raise HTTPException(status_code=404, detail="Journal not found")
            
        # Security: verify ownership (journals usually have user_email)
        if journal.get("user_email") != current_user["email"]:
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this journal")
            
        return journal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def save_journal(journal: Journal, current_user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        # Security: override user_email from token
        journal_data = journal.model_dump()
        journal_data["user_email"] = current_user["email"]
        
        saved_journal = db.save_ai_journal(current_user["email"], journal_data)
        return saved_journal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{journal_id}")
async def delete_journal(journal_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        success = db.delete_journal(current_user["email"], journal_id)
        if not success:
            raise HTTPException(status_code=404, detail="Journal not found")
        return {"message": "Journal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

