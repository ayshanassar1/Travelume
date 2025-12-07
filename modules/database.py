"""
Database Module for Travelume
Handles user data, trips, and persistence with JSON storage
Integrated with your existing main.py authentication system
"""

import json
import os
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import streamlit as st

class Database:
    """JSON-based database for Travelume that works with your current main.py"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.trips_file = os.path.join(data_dir, "trips.json")
        self.community_file = os.path.join(data_dir, "community.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize files
        self._init_files()
        
        # Load data
        self.users = self._load_json(self.users_file, default={})
        self.trips = self._load_json(self.trips_file, default={})
        self.community_plans = self._load_json(self.community_file, default=[])
    
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
    
    def _load_json(self, filepath: str, default=None):
        """Load JSON file with error handling"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return default if default is not None else {}
    
    def _save_json(self, filepath: str, data):
        """Save data to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    # ---------- USER MANAGEMENT (INTEGRATES WITH YOUR MAIN.PY) ----------
    
    def hash_password(self, password: str) -> str:
        """Simple password hashing - matches your main.py logic"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email: str, password: str, name: str, **extra_data) -> Dict:
        """Create a new user - works with your HTML auth page"""
        if email in self.users:
            raise ValueError(f"User {email} already exists")
        
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": email,
            "password": password,  # Keep plain password for your main.py compatibility
            "name": name,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "trips": [],  # List of trip IDs
            "saved_destinations": [],
            "travel_buddies": [],
            "preferences": {
                "theme": "Not set",
                "budget_range": "Not set",
                "favorite_destinations": []
            },
            **extra_data
        }
        
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
        
        # Don't allow updating email or password through this method
        for key, value in updates.items():
            if key not in ["email", "password"]:
                self.users[email][key] = value
        
        self.users[email]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_json(self.users_file, self.users)
        
        # Also update session state
        if "users" in st.session_state and email in st.session_state.users:
            for key, value in updates.items():
                if key not in ["email", "password"]:
                    st.session_state.users[email][key] = value
        
        return True
    
    def update_user_password(self, email: str, new_password: str) -> bool:
        """Update user password"""
        if email not in self.users:
            return False
        
        self.users[email]["password"] = new_password
        self.users[email]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_json(self.users_file, self.users)
        
        # Update session state
        if "users" in st.session_state and email in st.session_state.users:
            st.session_state.users[email]["password"] = new_password
        
        return True
    
    # ---------- TRIP MANAGEMENT (FOR AI PLANNER) ----------
    
    def save_ai_trip(self, user_email: str, trip_data: Dict) -> str:
        """
        Save a trip generated by AI planner
        trip_data should contain all info from ai_planner.py
        """
        trip_id = f"trip_{uuid.uuid4().hex[:8]}"
        
        full_trip_data = {
            "id": trip_id,
            "user_email": user_email,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "saved",
            **trip_data
        }
        
        # Save to trips database
        self.trips[trip_id] = full_trip_data
        self._save_json(self.trips_file, self.trips)
        
        # Add trip ID to user's trips list
        if user_email in self.users:
            if "trips" not in self.users[user_email]:
                self.users[user_email]["trips"] = []
            
            if trip_id not in self.users[user_email]["trips"]:
                self.users[user_email]["trips"].append(trip_id)
                self._save_json(self.users_file, self.users)
        
        # Update session state
        if "users" in st.session_state and user_email in st.session_state.users:
            if "trips" not in st.session_state.users[user_email]:
                st.session_state.users[user_email]["trips"] = []
            st.session_state.users[user_email]["trips"].append(trip_id)
        
        return trip_id
    
    def get_user_trips(self, user_email: str) -> List[Dict]:
        """Get all trips for a specific user"""
        if user_email not in self.users:
            return []
        
        trip_ids = self.users[user_email].get("trips", [])
        user_trips = []
        
        for trip_id in trip_ids:
            if trip_id in self.trips:
                user_trips.append(self.trips[trip_id])
        
        # Sort by creation date (newest first)
        user_trips.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return user_trips
    
    def get_trip_details(self, trip_id: str) -> Optional[Dict]:
        """Get detailed trip information"""
        return self.trips.get(trip_id)
    
    def delete_trip(self, user_email: str, trip_id: str) -> bool:
        """Delete a trip"""
        if trip_id not in self.trips:
            return False
        
        # Remove from trips database
        del self.trips[trip_id]
        self._save_json(self.trips_file, self.trips)
        
        # Remove from user's trips list
        if user_email in self.users and "trips" in self.users[user_email]:
            self.users[user_email]["trips"] = [
                tid for tid in self.users[user_email]["trips"] if tid != trip_id
            ]
            self._save_json(self.users_file, self.users)
        
        # Update session state
        if "users" in st.session_state and user_email in st.session_state.users:
            if "trips" in st.session_state.users[user_email]:
                st.session_state.users[user_email]["trips"] = [
                    tid for tid in st.session_state.users[user_email]["trips"] if tid != trip_id
                ]
        
        return True
    
    def update_trip(self, trip_id: str, **updates) -> bool:
        """Update trip information"""
        if trip_id not in self.trips:
            return False
        
        self.trips[trip_id].update(updates)
        self.trips[trip_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_json(self.trips_file, self.trips)
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
    print(f"Database initialized: {len(db.users)} users, {len(db.trips)} trips")
    return db