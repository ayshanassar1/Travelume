from fastapi import APIRouter, HTTPException, Depends
from typing import List
import sys
import os
from datetime import datetime

# Import Database and Models
from modules.database import get_database
from backend.models import Trip
from backend.routers.auth import get_current_user

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


@router.get("/")
async def get_trips(current_user: dict = Depends(get_current_user)):
    user_email = current_user["email"]
    db = get_database()
    try:
        return db.get_user_trips(user_email)
    except Exception as e:
        # Structured logging handled in db.get_user_trips
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{trip_id}")
async def get_trip(trip_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        trip = db.get_trip_details(trip_id)
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        
        # Security: verify ownership
        if trip.get("user_email") != current_user["email"]:
            raise HTTPException(status_code=403, detail="Forbidden: You do not own this trip")
            
        return trip
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def save_trip(trip: Trip, current_user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        # Security: override user_email from token
        trip_data = trip.model_dump()
        trip_data["user_email"] = current_user["email"]
        
        trip_id = db.save_ai_trip(current_user["email"], trip_data)
        return {"id": trip_id, "message": "Trip saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{trip_id}")
async def delete_trip(trip_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    try:
        success = db.delete_trip(current_user["email"], trip_id)
        if not success:
            raise HTTPException(status_code=404, detail="Trip not found")
        return {"message": "Trip deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

