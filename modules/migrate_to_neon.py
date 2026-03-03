import os
import json
import sys
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.database import get_database
from modules.models import User, Trip, Journal, CommunityPlan

def migrate_data():
    db = get_database()
    if not db.engine:
        print("Error: DATABASE_URL not found or connection failed. Please set it in your .env file.")
        return

    session = db.get_session()
    if not session:
        print("Error: Could not establish a database session.")
        return

    print("--- Starting Migration to NeonDB ---")

    try:
        # 1. Migrate Users
        print(f"Migrating {len(db.users)} users...")
        for email, u in db.users.items():
            existing = session.query(User).filter(User.email == email).first()
            if not existing:
                db_user = User(
                    email=email,
                    name=u.get("name"),
                    password=u.get("password"),
                    created_at=u.get("created_at"),
                    preferences=u.get("preferences", {})
                )
                session.add(db_user)
        session.commit()
        print("Users migrated successfully.")

        # 2. Migrate Trips
        print(f"Migrating {len(db.trips)} trips...")
        for trip_id, t in db.trips.items():
            existing = session.query(Trip).filter(Trip.id == trip_id).first()
            if not existing:
                db_trip = Trip(
                    id=trip_id,
                    user_email=t.get("user_email"),
                    created_at=t.get("created_at"),
                    status=t.get("status", "saved"),
                    name=t.get("name"),
                    destination=t.get("destination"),
                    duration=str(t.get("duration")),
                    budget=str(t.get("budget")),
                    itinerary_data=t.get("itinerary_data"),
                    planner_form=t.get("planner_form")
                )
                session.add(db_trip)
        session.commit()
        print("Trips migrated successfully.")

        # 3. Migrate Journals
        journals_dict = db.journals.get("journals", {})
        print(f"Migrating {len(journals_dict)} journals...")
        for j_id, j in journals_dict.items():
            existing = session.query(Journal).filter(Journal.id == j_id).first()
            if not existing:
                db_journal = Journal(
                    id=j_id,
                    user_email=j.get("user_email"),
                    title=j.get("title"),
                    country=j.get("country"),
                    description=j.get("description"),
                    startDate=j.get("startDate"),
                    endDate=j.get("endDate"),
                    companions=j.get("companions"),
                    ratings=j.get("ratings", 0),
                    bestMemory=j.get("bestMemory"),
                    travelStory=j.get("travelStory"),
                    unforgettableMemory=j.get("unforgettableMemory"),
                    memoryDate=j.get("memoryDate"),
                    bestMemoryImg=j.get("bestMemoryImg"),
                    tripImgs=j.get("tripImgs", []),
                    dailyImgs=j.get("dailyImgs", []),
                    foodImg=j.get("foodImg"),
                    videoUrl=j.get("videoUrl"),
                    lastFaveImg=j.get("lastFaveImg"),
                    tripDays=j.get("tripDays", 0),
                    is_public=j.get("is_public", False),
                    tags=j.get("tags", []),
                    trip_id=j.get("trip_id"),
                    photos=j.get("photos", []),
                    ppts=j.get("ppts", []),
                    created_at=j.get("created_at"),
                    updated_at=j.get("updated_at"),
                    views=j.get("views", 0),
                    pdf_generated=j.get("pdf_generated", False),
                    pdf_path=j.get("pdf_path")
                )
                session.add(db_journal)
        session.commit()
        print("Journals migrated successfully.")

        # 4. Migrate Community Plans
        print(f"Migrating {len(db.community_plans)} community plans...")
        for p in db.community_plans:
            p_id = p.get("id")
            existing = session.query(CommunityPlan).filter(CommunityPlan.id == p_id).first()
            if not existing:
                db_plan = CommunityPlan(
                    id=p_id,
                    destination=p.get("destination"),
                    title=p.get("title"),
                    creator=p.get("creator"),
                    likes=p.get("likes", 0),
                    saves=p.get("saves", 0),
                    budget_range=p.get("budget_range"),
                    duration=p.get("duration"),
                    image_url=p.get("image_url"),
                    popularity=p.get("popularity", 0)
                )
                session.add(db_plan)
        session.commit()
        print("Community plans migrated successfully.")

        print("--- Migration Finished Successfully! ---")

    except Exception as e:
        print(f"An error occurred during migration: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    migrate_data()