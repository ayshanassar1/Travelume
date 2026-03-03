from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr
    token: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str

class JournalBase(BaseModel):
    title: str
    description: str
    is_public: bool = False
    tags: List[str] = []
    trip_id: Optional[str] = None

class JournalCreate(JournalBase):
    pass

class JournalUpdate(JournalBase):
    pass

class Journal(BaseModel):
    id: Optional[str] = None
    user_email: str
    title: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    companions: Optional[str] = None
    ratings: Optional[int] = 0
    bestMemory: Optional[str] = None
    travelStory: Optional[str] = None
    unforgettableMemory: Optional[str] = None
    memoryDate: Optional[str] = None
    bestMemoryImg: Optional[str] = None
    tripImgs: List[Optional[str]] = []
    dailyImgs: List[List[Optional[str]]] = []
    foodImg: Optional[str] = None
    videoUrl: Optional[str] = None
    lastFaveImg: Optional[str] = None
    tripDays: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    views: int = 0
    is_public: bool = False
    tags: List[str] = []
    pdf_generated: bool = False
    pdf_path: Optional[str] = None
    trip_id: Optional[str] = None

    class Config:
        extra = "allow"

class AIPlannerForm(BaseModel):
    departure_city: str
    destination: str
    start_date: str
    end_date: str
    travel_theme: str
    travel_pace: str
    weather_preference: Optional[str] = "Normal"
    accommodation_type: str
    food_preferences: List[str]
    travel_mode: str
    currency: str
    budget: float
    passengers: int
    additional_prefs: Optional[str] = None
    refinement: Optional[str] = None

class Trip(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    destination: Optional[str] = None
    duration: Optional[str] = None
    budget: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    itinerary_data: Optional[dict] = None
    planner_form: Optional[dict] = None
    user_email: Optional[str] = None
    # Legacy Streamlit-era fields
    departure_city: Optional[str] = None
    duration_days: Optional[int] = None
    budget_per_person: Optional[float] = None
    total_budget: Optional[float] = None
    passengers: Optional[int] = None
    itinerary: Optional[dict] = None
    notes: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    travel_theme: Optional[str] = None
    travel_mode: Optional[str] = None
    type: Optional[str] = None
    ai_generated: Optional[bool] = None
    status: Optional[str] = None
    created_date: Optional[str] = None

    class Config:
        extra = "allow"
