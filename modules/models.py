from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    email = Column(String, primary_key=True)
    name = Column(String)
    password = Column(String)
    created_at = Column(String)
    preferences = Column(JSON, default={})
    
    trips = relationship("Trip", back_populates="user")
    journals = relationship("Journal", back_populates="user")

class Trip(Base):
    __tablename__ = 'trips'
    
    id = Column(String, primary_key=True)
    user_email = Column(String, ForeignKey('users.email'))
    created_at = Column(String)
    status = Column(String)
    name = Column(String)
    destination = Column(String)
    duration = Column(String)
    budget = Column(String)
    itinerary_data = Column(JSON)
    planner_form = Column(JSON)
    
    user = relationship("User", back_populates="trips")

class Journal(Base):
    __tablename__ = 'journals'
    
    id = Column(String, primary_key=True)
    user_email = Column(String, ForeignKey('users.email'))
    title = Column(String)
    country = Column(String)
    description = Column(String)
    startDate = Column(String)
    endDate = Column(String)
    companions = Column(String)
    ratings = Column(Integer, default=0)
    bestMemory = Column(String)
    travelStory = Column(String)
    unforgettableMemory = Column(String)
    memoryDate = Column(String)
    bestMemoryImg = Column(String)
    tripImgs = Column(JSON, default=[])
    dailyImgs = Column(JSON, default=[])
    foodImg = Column(String)
    videoUrl = Column(String)
    lastFaveImg = Column(String)
    tripDays = Column(Integer, default=0)
    is_public = Column(Boolean, default=False)
    tags = Column(JSON, default=[])
    trip_id = Column(String)
    photos = Column(JSON, default=[])
    ppts = Column(JSON, default=[])
    created_at = Column(String)
    updated_at = Column(String)
    views = Column(Integer, default=0)
    pdf_generated = Column(Boolean, default=False)
    pdf_path = Column(String, nullable=True)
    
    user = relationship("User", back_populates="journals")

class CommunityPlan(Base):
    __tablename__ = 'community_plans'
    
    id = Column(String, primary_key=True)
    destination = Column(String)
    title = Column(String)
    creator = Column(String)
    likes = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    budget_range = Column(String)
    duration = Column(String)
    image_url = Column(String)
    popularity = Column(Integer, default=0)
