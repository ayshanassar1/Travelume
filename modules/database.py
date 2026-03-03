"""
Database Module for Travelume
Handles user data, trips, journals and persistence with JSON storage
Integrated with your existing main.py authentication system
"""

import json
import os
import uuid
import hashlib
import base64
import re
import tempfile
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import streamlit as st

logger = logging.getLogger("travelume.database")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, User as DBUser, Trip as DBTrip, Journal as DBJournal, CommunityPlan as DBCommunityPlan

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Check travelume/.env specifically if not in global env
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        load_dotenv(env_path)
        DATABASE_URL = os.getenv("DATABASE_URL")
    except ImportError:
        pass

class Database:
    """JSON-based database for Travelume that works with your current main.py"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Get the directory of this file (travelume/modules)
            module_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to travelume and then into data
            self.data_dir = os.path.join(os.path.dirname(module_dir), "data")
        else:
            self.data_dir = data_dir
        
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.trips_file = os.path.join(self.data_dir, "trips.json")
        self.community_file = os.path.join(self.data_dir, "community.json")
        self.journals_file = os.path.join(self.data_dir, "journals.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize SQLAlchemy if URL is available
        self.engine = None
        self.SessionLocal = None
        if DATABASE_URL:
            try:
                # Neon requires SSL for external connections
                connect_args = {}
                if "sslmode" not in DATABASE_URL:
                    if "?" in DATABASE_URL:
                        temp_url = DATABASE_URL + "&sslmode=require"
                    else:
                        temp_url = DATABASE_URL + "?sslmode=require"
                else:
                    temp_url = DATABASE_URL
                
                self.engine = create_engine(temp_url, connect_args=connect_args)
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                # Create tables if they don't exist
                Base.metadata.create_all(bind=self.engine)
            except Exception as e:
                print(f"Failed to connect to NeonDB: {e}. Falling back to JSON.")
                self.engine = None
                self.SessionLocal = None
        
        # Initialize files
        self._init_files()
        
        # Load data
        self.users = self._load_json(self.users_file, default={})
        self.trips = self._load_json(self.trips_file, default={})
        self.community_plans = self._load_json(self.community_file, default=[])
        self.journals = self._load_json(self.journals_file, default={"journals": {}})
    
    def _init_files(self):
        """Initialize JSON files if they don't exist"""
        # Users file
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
        
        # Trips file
        if not os.path.exists(self.trips_file):
            with open(self.trips_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)
        
        # Community file with sample data
        if not os.path.exists(self.community_file):
            sample_plans = [
                {
                    "id": "dubai_plan_001",
                    "destination": "Dubai",
                    "title": "7-Day Luxury Dubai Experience",
                    "creator": "Travelume Community",
                    "likes": 245,
                    "saves": 120,
                    "budget_range": "₹60,000 - ₹1,25,000",
                    "duration": "7 days",
                    "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c",
                    "popularity": 95
                },
                {
                    "id": "thailand_plan_002",
                    "destination": "Thailand",
                    "title": "10-Day Thailand Adventure",
                    "creator": "Travelume Community",
                    "likes": 189,
                    "saves": 95,
                    "budget_range": "₹70,000 - ₹1,21,000",
                    "duration": "10 days",
                    "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a",
                    "popularity": 88
                },
                {
                    "id": "bali_plan_003",
                    "destination": "Bali",
                    "title": "8-Day Bali Tropical Escape",
                    "creator": "Travelume Community",
                    "likes": 312,
                    "saves": 156,
                    "budget_range": "₹45,000 - ₹80,000",
                    "duration": "8 days",
                    "image_url": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1",
                    "popularity": 92
                },
                {
                    "id": "paris_plan_004",
                    "destination": "Paris",
                    "title": "6-Day Romantic Paris Getaway",
                    "creator": "Travelume Community",
                    "likes": 278,
                    "saves": 134,
                    "budget_range": "₹60,000 - ₹90,000",
                    "duration": "6 days",
                    "image_url": "https://images.unsplash.com/photo-1502602898536-47ad22581b52",
                    "popularity": 90
                }
            ]
            with open(self.community_file, 'w', encoding='utf-8') as f:
                json.dump(sample_plans, f, indent=2)
        
        # Journals file
        if not os.path.exists(self.journals_file):
            with open(self.journals_file, 'w', encoding='utf-8') as f:
                json.dump({"journals": {}}, f, indent=2)
    
    def _load_json(self, filepath: str, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"[DB] Failed to load {filepath}: {e}. Returning default.")
        return default if default is not None else {}

    def _save_json(self, filepath: str, data):
        """Atomically save data to JSON file using temp file + rename to prevent corruption."""
        dir_ = os.path.dirname(filepath)
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                'w', dir=dir_, delete=False, suffix='.tmp', encoding='utf-8'
            ) as tf:
                json.dump(data, tf, indent=2)
                tmp_path = tf.name
            os.replace(tmp_path, filepath)  # Atomic on POSIX; near-atomic on Windows
        except Exception as e:
            logger.error(f"[DB] CRITICAL: Failed to save {filepath}: {e}")
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise
    
    def get_session(self) -> Optional[Session]:
        """Helper to get a database session"""
        if self.SessionLocal:
            return self.SessionLocal()
        return None

    # ---------- USER MANAGEMENT (INTEGRATES WITH YOUR MAIN.PY) ----------
    
    def hash_password(self, password: str) -> str:
        """Simple password hashing - matches your main.py logic"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email: str, password: str, name: str, **extra_data) -> Dict:
        """Create a new user - works with your HTML auth page and NeonDB"""
        if email in self.users:
            raise ValueError(f"User {email} already exists")
        
        user_id = str(uuid.uuid4())
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data = {
            "id": user_id,
            "email": email,
            "password": password,  # Keep plain password for your main.py compatibility
            "name": name,
            "created_at": created_at,
            "trips": [],  # List of trip IDs
            "journals": [],  # List of journal IDs - NEW
            "saved_destinations": [],
            "travel_buddies": [],
            "preferences": {
                "theme": "Not set",
                "budget_range": "Not set",
                "favorite_destinations": [],
                **extra_data.get("preferences", {})
            }
        }
        
        # Save to NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_user = DBUser(
                    email=email,
                    name=name,
                    password=password,
                    created_at=created_at,
                    preferences=user_data["preferences"]
                )
                session.add(db_user)
                session.commit()
            except Exception as e:
                print(f"Error saving user to NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Update local cache and save to disk
        self.users[email] = user_data
        self._save_json(self.users_file, self.users)
        
        # Also update session state for immediate use
        if "users" not in st.session_state:
            st.session_state.users = {}
        st.session_state.users[email] = user_data
        
        # Return user data without password for security
        return_data = user_data.copy()
        del return_data["password"]
        return return_data
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user - works with your main.py validation"""
        user = self.users.get(email)
        
        if user and user.get("password") == password:  # Direct comparison for your main.py
            # Return user data without password
            user_data = user.copy()
            user_data.pop("password", None)
            return user_data
        return None
    
    def get_user(self, email: str) -> Optional[Dict]:
        """Get user by email (without password)"""
        user = self.users.get(email)
        if user:
            user_data = user.copy()
            user_data.pop("password", None)
            return user_data
        return None
    
    def update_user(self, email: str, **updates) -> bool:
        """Update user information"""
        if email not in self.users:
            return False
        
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update in NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_user = session.query(DBUser).filter(DBUser.email == email).first()
                if db_user:
                    for key, value in updates.items():
                        if hasattr(db_user, key) and key not in ["email", "password"]:
                            setattr(db_user, key, value)
                    db_user.updated_at = updated_at
                    session.commit()
            except Exception as e:
                print(f"Error updating user in NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Update locally
        for key, value in updates.items():
            if key not in ["email", "password"]:
                self.users[email][key] = value
        
        self.users[email]["updated_at"] = updated_at
        self._save_json(self.users_file, self.users)
        
        # Also update session state
        try:
            if "users" in st.session_state and email in st.session_state.users:
                for key, value in updates.items():
                    if key not in ["email", "password"]:
                        st.session_state.users[email][key] = value
        except Exception as e:
            logger.warning(f"[DB] Could not sync update_user to session_state for {email}: {e}")

        return True
    
    def update_user_password(self, email: str, new_password: str) -> bool:
        """Update user password"""
        if email not in self.users:
            return False
        
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update in NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_user = session.query(DBUser).filter(DBUser.email == email).first()
                if db_user:
                    db_user.password = new_password
                    db_user.updated_at = updated_at
                    session.commit()
            except Exception as e:
                print(f"Error updating password in NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Update locally
        self.users[email]["password"] = new_password
        self.users[email]["updated_at"] = updated_at
        self._save_json(self.users_file, self.users)
        
        # Update session state
        try:
            if "users" in st.session_state and email in st.session_state.users:
                st.session_state.users[email]["password"] = new_password
        except:
            pass
        
        return True

    def sync_from_db(self):
        """Sync local JSON cache from NeonDB"""
        session = self.get_session()
        if not session:
            return
            
        try:
            # Sync Users
            db_users = session.query(DBUser).all()
            for u in db_users:
                if u.email not in self.users:
                    self.users[u.email] = {
                        "id": str(uuid.uuid4()),
                        "email": u.email,
                        "name": u.name,
                        "password": u.password,
                        "created_at": u.created_at,
                        "preferences": u.preferences,
                        "trips": [],
                        "journals": []
                    }
            
            # Sync Trips
            db_trips = session.query(DBTrip).all()
            for t in db_trips:
                if t.id not in self.trips:
                    self.trips[t.id] = {
                        "id": t.id,
                        "user_email": t.user_email,
                        "created_at": t.created_at,
                        "status": t.status,
                        "name": t.name,
                        "destination": t.destination,
                        "duration": t.duration,
                        "budget": t.budget,
                        "itinerary_data": t.itinerary_data,
                        "planner_form": t.planner_form
                    }
                    # Ensure user's trip list is updated
                    if t.user_email in self.users and t.id not in self.users[t.user_email].get("trips", []):
                        if "trips" not in self.users[t.user_email]:
                            self.users[t.user_email]["trips"] = []
                        self.users[t.user_email]["trips"].append(t.id)

            # Save synced data locally
            self._save_json(self.users_file, self.users)
            self._save_json(self.trips_file, self.trips)
            print("Successfully synced data from NeonDB to local JSON.")
            
        except Exception as e:
            print(f"Error syncing from NeonDB: {e}")
        finally:
            session.close()

    # ---------- TRIP MANAGEMENT (FOR AI PLANNER) ----------
    
    def save_ai_trip(self, user_email: str, trip_data: Dict) -> str:
        """
        Save a trip generated by AI planner
        trip_data should contain all info from ai_planner.py
        """
        trip_id = trip_data.get("id") or f"trip_{uuid.uuid4().hex[:8]}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare full trip record
        full_trip_data = {
            "id": trip_id,
            "user_email": user_email,
            "created_at": created_at,
            "status": "saved",
            "name": trip_data.get("name", "Unnamed Trip"),
            "destination": trip_data.get("destination", "Unknown"),
            "duration": trip_data.get("duration", "Not set"),
            "budget": trip_data.get("budget", "Not set"),
            "itinerary_data": trip_data.get("itinerary_data", {}),
            "planner_form": trip_data.get("planner_form", {})
        }
        
        # Save to NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_trip = DBTrip(
                    id=trip_id,
                    user_email=user_email,
                    created_at=created_at,
                    status="saved",
                    name=full_trip_data["name"],
                    destination=full_trip_data["destination"],
                    duration=str(full_trip_data["duration"]),
                    budget=str(full_trip_data["budget"]),
                    itinerary_data=full_trip_data["itinerary_data"],
                    planner_form=full_trip_data["planner_form"]
                )
                session.add(db_trip)
                session.commit()
            except Exception as e:
                print(f"Error saving trip to NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Save to trips database locally
        self.trips[trip_id] = full_trip_data
        self._save_json(self.trips_file, self.trips)
        
        # Add trip ID to user's trips list
        if user_email in self.users:
            if "trips" not in self.users[user_email]:
                self.users[user_email]["trips"] = []
            
            if trip_id not in self.users[user_email]["trips"]:
                self.users[user_email]["trips"].append(trip_id)
                self._save_json(self.users_file, self.users)
        
        # Update session state if in Streamlit
        try:
            if "users" in st.session_state and user_email in st.session_state.users:
                if "trips" not in st.session_state.users[user_email]:
                    st.session_state.users[user_email]["trips"] = []
                # De-duplicate before appending
                if trip_id not in st.session_state.users[user_email]["trips"]:
                    st.session_state.users[user_email]["trips"].append(trip_id)
        except Exception as e:
            logger.warning(f"[DB] Could not sync save_ai_trip to session_state for {user_email}: {e}")

        return trip_id
    
    def get_user_trips(self, user_email: str) -> List[Dict]:
        """Get all trips for a specific user, merging NeonDB and JSON sources."""
        user_trips = []
        seen_ids = set()

        # 1. Try NeonDB
        session = self.get_session()
        if session:
            try:
                db_trips = session.query(DBTrip).filter(DBTrip.user_email == user_email).all()
                for t in db_trips:
                    if t.id not in seen_ids:
                        user_trips.append({
                            "id": t.id,
                            "user_email": t.user_email,
                            "created_at": t.created_at,
                            "status": t.status,
                            "name": t.name,
                            "destination": t.destination,
                            "duration": t.duration,
                            "budget": t.budget,
                            "itinerary_data": t.itinerary_data,
                            "planner_form": t.planner_form
                        })
                        seen_ids.add(t.id)
                logger.info(f"[DB] get_user_trips({user_email}): Found {len(db_trips)} records in NeonDB.")
            except Exception as e:
                logger.error(f"[DB] NeonDB query failed for trips ({user_email}): {e}")
            finally:
                session.close()

        # 2. JSON Fallback - Merge with data from users.json reference
        if user_email in self.users:
            trip_ids = self.users[user_email].get("trips", [])
            for trip_id in trip_ids:
                if trip_id in self.trips and trip_id not in seen_ids:
                    user_trips.append(self.trips[trip_id])
                    seen_ids.add(trip_id)

        # 3. Secondary scan - catch trips not referenced in user record but exist in trips.json
        for trip_id, trip_data in self.trips.items():
            if trip_data.get("user_email") == user_email and trip_id not in seen_ids:
                user_trips.append(trip_data)
                seen_ids.add(trip_id)

        user_trips.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        return user_trips

    
    def get_trip_details(self, trip_id: str) -> Optional[Dict]:
        """Get detailed trip information"""
        return self.trips.get(trip_id)
    
    def delete_trip(self, user_email: str, trip_id: str) -> bool:
        """Delete a trip"""
        if trip_id not in self.trips:
            return False
        
        # Delete from NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_trip = session.query(DBTrip).filter(DBTrip.id == trip_id).first()
                if db_trip:
                    session.delete(db_trip)
                    session.commit()
            except Exception as e:
                print(f"Error deleting trip from NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Remove from trips database locally
        del self.trips[trip_id]
        self._save_json(self.trips_file, self.trips)
        
        # Remove from user's trips list
        if user_email in self.users and "trips" in self.users[user_email]:
            self.users[user_email]["trips"] = [
                tid for tid in self.users[user_email]["trips"] if tid != trip_id
            ]
            self._save_json(self.users_file, self.users)
        
        # Update session state
        try:
            if "users" in st.session_state and user_email in st.session_state.users:
                if "trips" in st.session_state.users[user_email]:
                    st.session_state.users[user_email]["trips"] = [
                        tid for tid in st.session_state.users[user_email]["trips"] if tid != trip_id
                    ]
        except:
            pass
        
        return True
    
    def update_trip(self, trip_id: str, **updates) -> bool:
        """Update trip information"""
        if trip_id not in self.trips:
            return False
        
        self.trips[trip_id].update(updates)
        self.trips[trip_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_json(self.trips_file, self.trips)
        return True
    
    # ---------- JOURNAL MANAGEMENT ----------
    
    def create_journal(self, user_email: str, title: str, description: str, 
                      photos: List[str] = None, trip_id: str = None) -> str:
        """Create a new travel journal"""
        journal_id = f"journal_{uuid.uuid4().hex[:8]}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        journal_data = {
            "id": journal_id,
            "user_email": user_email,
            "title": title,
            "description": description,
            "photos": photos or [],
            "trip_id": trip_id,
            "created_at": created_at,
            "updated_at": created_at,
            "views": 0,
            "is_public": False,
            "tags": [],
            "pdf_generated": False,
            "pdf_path": None
        }
        
        # Save to NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_journal = DBJournal(
                    id=journal_id,
                    user_email=user_email,
                    title=title,
                    description=description,
                    is_public=False,
                    tags=[],
                    trip_id=trip_id,
                    photos=journal_data["photos"],
                    ppts=[],
                    created_at=created_at,
                    updated_at=created_at,
                    views=0,
                    pdf_generated=False,
                    pdf_path=None
                )
                session.add(db_journal)
                session.commit()
            except Exception as e:
                print(f"Error saving journal to NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Save to journals database locally
        if "journals" not in self.journals:
            self.journals["journals"] = {}
        
        self.journals["journals"][journal_id] = journal_data
        self._save_json(self.journals_file, self.journals)
        
        # Add journal ID to user's journals list
        if user_email in self.users:
            if "journals" not in self.users[user_email]:
                self.users[user_email]["journals"] = []
            
            if journal_id not in self.users[user_email]["journals"]:
                self.users[user_email]["journals"].append(journal_id)
                self._save_json(self.users_file, self.users)
        
        # Update session state if in Streamlit
        try:
            if "users" in st.session_state and user_email in st.session_state.users:
                if "journals" not in st.session_state.users[user_email]:
                    st.session_state.users[user_email]["journals"] = []
                # De-duplicate before appending
                if journal_id not in st.session_state.users[user_email]["journals"]:
                    st.session_state.users[user_email]["journals"].append(journal_id)
        except Exception as e:
            logger.warning(f"[DB] Could not sync create_journal to session_state for {user_email}: {e}")

        return journal_id
    
    def get_user_journals(self, user_email: str) -> List[Dict]:
        """Get all journals for a specific user, merging NeonDB and JSON sources."""
        user_journals = []
        seen_ids = set()

        # 1. Try NeonDB
        session = self.get_session()
        if session:
            try:
                db_journals = session.query(DBJournal).filter(DBJournal.user_email == user_email).all()
                for j in db_journals:
                    if j.id not in seen_ids:
                        user_journals.append({
                            "id": j.id,
                            "user_email": j.user_email,
                            "title": j.title,
                            "country": j.country,
                            "description": j.description,
                            "startDate": j.startDate,
                            "endDate": j.endDate,
                            "companions": j.companions,
                            "ratings": j.ratings,
                            "bestMemory": j.bestMemory,
                            "travelStory": j.travelStory,
                            "unforgettableMemory": j.unforgettableMemory,
                            "memoryDate": j.memoryDate,
                            "bestMemoryImg": j.bestMemoryImg,
                            "tripImgs": j.tripImgs,
                            "dailyImgs": j.dailyImgs,
                            "foodImg": j.foodImg,
                            "videoUrl": j.videoUrl,
                            "lastFaveImg": j.lastFaveImg,
                            "tripDays": j.tripDays,
                            "is_public": j.is_public,
                            "tags": j.tags,
                            "trip_id": j.trip_id,
                            "photos": j.photos,
                            "ppts": j.ppts,
                            "created_at": j.created_at,
                            "updated_at": j.updated_at,
                            "views": j.views,
                            "pdf_generated": j.pdf_generated,
                            "pdf_path": j.pdf_path
                        })
                        seen_ids.add(j.id)
                logger.info(f"[DB] get_user_journals({user_email}): Found {len(db_journals)} records in NeonDB.")
            except Exception as e:
                logger.error(f"[DB] NeonDB query failed for journals ({user_email}): {e}")
            finally:
                session.close()

        # 2. JSON Fallback - Merge with data from users.json reference
        if user_email in self.users:
            journal_ids = self.users[user_email].get("journals", [])
            for journal_id in journal_ids:
                if journal_id not in seen_ids:
                    journal = self.get_journal(journal_id)
                    if journal:
                        user_journals.append(journal)
                        seen_ids.add(journal_id)

        # 3. Secondary scan - catch journals in journals.json
        all_journals = self.journals.get("journals", {})
        for journal_id, journal_data in all_journals.items():
            if journal_data.get("user_email") == user_email and journal_id not in seen_ids:
                user_journals.append(journal_data)
                seen_ids.add(journal_id)

        user_journals.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        return user_journals

    
    def get_journal(self, journal_id: str) -> Optional[Dict]:
        """Get detailed journal information"""
        if "journals" not in self.journals:
            return None
        return self.journals.get("journals", {}).get(journal_id)
    
    def update_journal(self, journal_id: str, **updates) -> bool:
        """Update journal information"""
        if "journals" not in self.journals or journal_id not in self.journals.get("journals", {}):
            return False
        
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update in NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_journal = session.query(DBJournal).filter(DBJournal.id == journal_id).first()
                if db_journal:
                    for key, value in updates.items():
                        if hasattr(db_journal, key):
                            setattr(db_journal, key, value)
                    db_journal.updated_at = updated_at
                    session.commit()
            except Exception as e:
                print(f"Error updating journal in NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Update locally
        self.journals["journals"][journal_id].update(updates)
        self.journals["journals"][journal_id]["updated_at"] = updated_at
        self._save_json(self.journals_file, self.journals)
        return True

    def delete_journal(self, user_email: str, journal_id: str) -> bool:
        """Delete a travel journal"""
        if "journals" not in self.journals or journal_id not in self.journals.get("journals", {}):
            return False
        
        # Delete from NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_journal = session.query(DBJournal).filter(DBJournal.id == journal_id).first()
                if db_journal:
                    session.delete(db_journal)
                    session.commit()
            except Exception as e:
                print(f"Error deleting journal from NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Remove from journals database locally
        del self.journals["journals"][journal_id]
        self._save_json(self.journals_file, self.journals)
        
        # Remove from user's journals list
        if user_email in self.users and "journals" in self.users[user_email]:
            self.users[user_email]["journals"] = [
                jid for jid in self.users[user_email]["journals"] if jid != journal_id
            ]
            self._save_json(self.users_file, self.users)
            
        return True
    
    def save_ai_journal(self, user_email: str, journal_data: Dict) -> str:
        """Save a new AI-generated/custom travel journal"""
        journal_id = journal_data.get("id") or f"journal_{uuid.uuid4().hex[:8]}"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Process images (convert base64 to files)
        journal_data = self._process_journal_images(user_email, journal_data)
        
        # Prepare full journal record
        full_journal_data = {
            "id": journal_id,
            "user_email": user_email,
            "created_at": created_at,
            "updated_at": created_at,
            "views": 0,
            "pdf_generated": False,
            "pdf_path": None,
            **journal_data
        }
        
        # Save to NeonDB if available
        session = self.get_session()
        if session:
            try:
                db_journal = DBJournal(
                    id=journal_id,
                    user_email=user_email,
                    title=full_journal_data.get("title"),
                    country=full_journal_data.get("country"),
                    description=full_journal_data.get("description"),
                    startDate=full_journal_data.get("startDate"),
                    endDate=full_journal_data.get("endDate"),
                    companions=full_journal_data.get("companions"),
                    ratings=full_journal_data.get("ratings", 0),
                    bestMemory=full_journal_data.get("bestMemory"),
                    travelStory=full_journal_data.get("travelStory"),
                    unforgettableMemory=full_journal_data.get("unforgettableMemory"),
                    memoryDate=full_journal_data.get("memoryDate"),
                    bestMemoryImg=full_journal_data.get("bestMemoryImg"),
                    tripImgs=full_journal_data.get("tripImgs", []),
                    dailyImgs=full_journal_data.get("dailyImgs", []),
                    foodImg=full_journal_data.get("foodImg"),
                    videoUrl=full_journal_data.get("videoUrl"),
                    lastFaveImg=full_journal_data.get("lastFaveImg"),
                    tripDays=full_journal_data.get("tripDays", 0),
                    is_public=full_journal_data.get("is_public", False),
                    tags=full_journal_data.get("tags", []),
                    trip_id=full_journal_data.get("trip_id"),
                    photos=full_journal_data.get("photos", []),
                    ppts=full_journal_data.get("ppts", []),
                    created_at=created_at,
                    updated_at=created_at,
                    views=0,
                    pdf_generated=False,
                    pdf_path=None
                )
                session.add(db_journal)
                session.commit()
            except Exception as e:
                print(f"Error saving journal to NeonDB: {e}")
                session.rollback()
            finally:
                session.close()

        # Save locally
        if "journals" not in self.journals:
            self.journals["journals"] = {}
        
        self.journals["journals"][journal_id] = full_journal_data
        self._save_json(self.journals_file, self.journals)
        
        # Add journal ID to user's journals list
        if user_email in self.users:
            if "journals" not in self.users[user_email]:
                self.users[user_email]["journals"] = []
            
            if journal_id not in self.users[user_email]["journals"]:
                self.users[user_email]["journals"].append(journal_id)
                self._save_json(self.users_file, self.users)
        
        return full_journal_data

    def _process_journal_images(self, user_email: str, journal_data: Dict) -> Dict:
        """Scan journal data for base64 images and save them to disk"""
        # Directory for images
        images_dir = os.path.join(self.data_dir, "journals", "images", user_email.replace("@", "_"))
        os.makedirs(images_dir, exist_ok=True)
        
        def save_base64_img(base64_str):
            if not isinstance(base64_str, str) or not base64_str.startswith("data:image"):
                return base64_str
            
            try:
                # Extract format and data
                match = re.match(r'data:image/([\w\+\.-]+);base64,(.*)', base64_str)
                if not match:
                    return base64_str
                
                ext = match.group(1)
                img_data = base64.b64decode(match.group(2))
                
                # Generate filename
                filename = f"{uuid.uuid4().hex}.{ext}"
                filepath = os.path.join(images_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(img_data)
                
                # Return relative path for frontend (served via /static/)
                rel_path = os.path.relpath(filepath, self.data_dir)
                return rel_path.replace("\\", "/") # Ensure forward slashes for URLs
            except Exception as e:
                print(f"Error saving base64 image: {e}")
                return base64_str

        # Process tripImgs
        if "tripImgs" in journal_data and isinstance(journal_data["tripImgs"], list):
            journal_data["tripImgs"] = [save_base64_img(img) for img in journal_data["tripImgs"]]
            
        # Process bestMemoryImg
        if "bestMemoryImg" in journal_data:
            journal_data["bestMemoryImg"] = save_base64_img(journal_data["bestMemoryImg"])
            
        # Process dailyImgs
        if "dailyImgs" in journal_data and isinstance(journal_data["dailyImgs"], list):
            new_daily_imgs = []
            for day_imgs in journal_data["dailyImgs"]:
                if isinstance(day_imgs, list):
                    new_daily_imgs.append([save_base64_img(img) for img in day_imgs])
                else:
                    new_daily_imgs.append(day_imgs)
            journal_data["dailyImgs"] = new_daily_imgs
            
        # Process foodImg
        if "foodImg" in journal_data:
            journal_data["foodImg"] = save_base64_img(journal_data["foodImg"])
            
        # Process lastFaveImg
        if "lastFaveImg" in journal_data:
            journal_data["lastFaveImg"] = save_base64_img(journal_data["lastFaveImg"])
            
        return journal_data

    def update_ai_journal(self, journal_id: str, updates: Dict) -> bool:
        """Update AI journal information"""
        if "journals" not in self.journals or journal_id not in self.journals.get("journals", {}):
            return False
        
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.journals["journals"][journal_id].update(updates)
        self.journals["journals"][journal_id]["updated_at"] = updated_at
        self._save_json(self.journals_file, self.journals)
        return True
    
    def add_photo_to_journal(self, journal_id: str, photo_url: str) -> bool:
        """Add a photo to a journal"""
        if journal_id not in self.journals.get("journals", {}):
            return False
        
        if "photos" not in self.journals["journals"][journal_id]:
            self.journals["journals"][journal_id]["photos"] = []
        
        self.journals["journals"][journal_id]["photos"].append(photo_url)
        self.journals["journals"][journal_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_json(self.journals_file, self.journals)
        return True
    
    def mark_pdf_generated(self, journal_id: str, pdf_path: str) -> bool:
        """Mark a journal as PDF generated"""
        if journal_id not in self.journals.get("journals", {}):
            return False
        
        self.journals["journals"][journal_id]["pdf_generated"] = True
        self.journals["journals"][journal_id]["pdf_path"] = pdf_path
        self.journals["journals"][journal_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_json(self.journals_file, self.journals)
        return True
    
    # ---------- COMMUNITY PLANS ----------
    
    def get_community_plans(self, limit: int = 10, sort_by: str = "popularity") -> List[Dict]:
        """Get community travel plans"""
        plans = self.community_plans.copy()
        
        if sort_by == "popularity":
            plans.sort(key=lambda x: x.get("popularity", 0), reverse=True)
        elif sort_by == "likes":
            plans.sort(key=lambda x: x.get("likes", 0), reverse=True)
        elif sort_by == "newest":
            plans.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return plans[:limit]
    
    def get_community_plan(self, plan_id: str) -> Optional[Dict]:
        """Get a specific community plan"""
        for plan in self.community_plans:
            if plan.get("id") == plan_id:
                return plan
        return None
    
    def like_community_plan(self, plan_id: str) -> bool:
        """Like a community plan"""
        for plan in self.community_plans:
            if plan.get("id") == plan_id:
                plan["likes"] = plan.get("likes", 0) + 1
                plan["popularity"] = plan.get("popularity", 0) + 5
                self._save_json(self.community_file, self.community_plans)
                return True
        return False
    
    def save_community_plan_to_user(self, user_email: str, plan_id: str) -> bool:
        """Save a community plan to user's saved destinations"""
        plan = self.get_community_plan(plan_id)
        if not plan:
            return False
        
        if user_email in self.users:
            if "saved_destinations" not in self.users[user_email]:
                self.users[user_email]["saved_destinations"] = []
            
            # Add if not already saved
            if plan_id not in self.users[user_email]["saved_destinations"]:
                self.users[user_email]["saved_destinations"].append(plan_id)
                self._save_json(self.users_file, self.users)
                
                # Update session state
                if "users" in st.session_state and user_email in st.session_state.users:
                    if "saved_destinations" not in st.session_state.users[user_email]:
                        st.session_state.users[user_email]["saved_destinations"] = []
                    st.session_state.users[user_email]["saved_destinations"].append(plan_id)
                
                # Increment save count on community plan
                for cp in self.community_plans:
                    if cp.get("id") == plan_id:
                        cp["saves"] = cp.get("saves", 0) + 1
                        cp["popularity"] = cp.get("popularity", 0) + 3
                        self._save_json(self.community_file, self.community_plans)
                        break
                
                return True
        return False
    
    # ---------- STATISTICS & UTILITIES ----------
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        total_trip_days = 0
        total_budget = 0
        
        for trip in self.trips.values():
            total_trip_days += trip.get("duration_days", 0)
            total_budget += trip.get("total_budget", 0)
        
        return {
            "total_users": len(self.users),
            "total_trips": len(self.trips),
            "total_journals": len(self.journals.get("journals", {})),
            "total_community_plans": len(self.community_plans),
            "total_trip_days": total_trip_days,
            "total_budget_planned": total_budget,
            "most_popular_destination": self._get_most_popular_destination()
        }
    
    def _get_most_popular_destination(self) -> str:
        """Get most popular destination from trips"""
        destinations = {}
        for trip in self.trips.values():
            dest = trip.get("destination", "Unknown")
            destinations[dest] = destinations.get(dest, 0) + 1
        
        if destinations:
            return max(destinations.items(), key=lambda x: x[1])[0]
        return "No trips yet"
    
    def sync_with_session_state(self):
        """Sync database with Streamlit session state"""
        # This ensures database and session state are in sync
        if "users" in st.session_state:
            for email, user_data in st.session_state.users.items():
                if email not in self.users:
                    self.users[email] = user_data
                else:
                    # Merge data, giving priority to session state
                    self.users[email].update(user_data)
            
            self._save_json(self.users_file, self.users)
    
    def backup_database(self, backup_dir: str = "backups") -> str:
        """Create a backup of the database"""
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"travelume_backup_{timestamp}.json")
        
        backup_data = {
            "timestamp": timestamp,
            "users": self.users,
            "trips": self.trips,
            "journals": self.journals,
            "community_plans": self.community_plans,
            "statistics": self.get_statistics()
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2)
        
        return backup_file

# Create a global database instance
_db_instance = None

def get_database():
    """Get or create database instance (singleton pattern)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance

# Quick test function
def test_database():
    """Test the database functions"""
    db = get_database()
    print(f"Database initialized: {len(db.users)} users, {len(db.trips)} trips, {len(db.journals.get('journals', {}))} journals")
    return db