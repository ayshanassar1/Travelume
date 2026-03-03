import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
import os
import re
import shelve
import logging

logger = logging.getLogger("travelume.travel_coach")

# Add project root to path if needed for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.llm_client import LLMClient
from modules.database import get_database
from modules.tts_service import TTSService


class TravelCoach:
    def __init__(self):
        self.llm = LLMClient()
        self.db = get_database()
        # Initialize TTS service with project root 'data' directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.tts = TTSService(os.path.join(project_root, "data"))
        # Path for disk-persisted session store (shelve creates .db/.dir/.bak files)
        self._session_store_path = os.path.join(project_root, "data", "chat_sessions")
        # Clean up stale sessions on startup
        self._cleanup_stale_sessions()

    # ------------------------------------------------------------------
    # Session persistence helpers (disk-backed via shelve)
    # ------------------------------------------------------------------

    def _load_session(self, session_id: str) -> Dict | None:
        """Load a session from disk. Returns None if not found."""
        try:
            with shelve.open(self._session_store_path) as store:
                return store.get(session_id)
        except Exception as e:
            logger.error(f"[TravelCoach] Failed to load session {session_id}: {e}")
            return None

    def _save_session(self, session_id: str, session: Dict):
        """Persist a session to disk."""
        try:
            # Convert datetime to ISO string for shelve serialisation
            session_copy = {**session}
            if isinstance(session_copy.get("start_time"), datetime):
                session_copy["start_time"] = session_copy["start_time"].isoformat()
            with shelve.open(self._session_store_path) as store:
                store[session_id] = session_copy
        except Exception as e:
            logger.error(f"[TravelCoach] Failed to save session {session_id}: {e}")

    def _delete_session(self, session_id: str):
        """Remove a session from disk."""
        try:
            with shelve.open(self._session_store_path) as store:
                if session_id in store:
                    del store[session_id]
        except Exception as e:
            logger.warning(f"[TravelCoach] Failed to delete session {session_id}: {e}")

    def _cleanup_stale_sessions(self, max_age_hours: int = 24):
        """Delete sessions older than max_age_hours to prevent disk bloat."""
        try:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            stale_ids = []
            with shelve.open(self._session_store_path) as store:
                for sid, session in store.items():
                    try:
                        start = session.get("start_time")
                        if isinstance(start, str):
                            start = datetime.fromisoformat(start)
                        if start and start < cutoff:
                            stale_ids.append(sid)
                    except Exception:
                        stale_ids.append(sid)  # Remove malformed sessions too

            for sid in stale_ids:
                self._delete_session(sid)

            if stale_ids:
                logger.info(f"[TravelCoach] Cleaned up {len(stale_ids)} stale sessions.")
        except Exception as e:
            logger.warning(f"[TravelCoach] Session cleanup warning: {e}")

    # ------------------------------------------------------------------
    # Audio file cleanup
    # ------------------------------------------------------------------

    def _cleanup_old_audio(self):
        """Deletes TTS audio files older than 1 hour to prevent disk accumulation."""
        try:
            audio_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "audio"
            )
            if not os.path.isdir(audio_dir):
                return
            cutoff = datetime.now().timestamp() - 3600  # 1 hour
            for fname in os.listdir(audio_dir):
                if fname.endswith(".mp3"):
                    fpath = os.path.join(audio_dir, fname)
                    if os.path.getmtime(fpath) < cutoff:
                        os.remove(fpath)
        except Exception as e:
            logger.warning(f"[TravelCoach] Audio cleanup warning: {e}")

    def start_session(self, user_email: str) -> Dict[str, Any]:
        """
        Initializes a travel coaching session with context.
        Session is persisted to disk so it survives backend restarts.
        """
        # Clean up old audio files on each new session start
        self._cleanup_old_audio()

        session_id = str(uuid.uuid4())

        # Get user context
        user_data = self.db.get_user(user_email)
        user_trips = self.db.get_user_trips(user_email)

        preferences = user_data.get("preferences", {}) if user_data else {}

        # Initial greeting
        name = user_data.get("name", "Traveler") if user_data else "Traveler"

        initial_text = (
            f"Hello {name}! I'm your Personal Travel Coach. "
            "I can help you plan your next trip, suggest destinations based on your preferences, "
            "or give you local tips. Where are you dreaming of going?"
        )
        initial_text = self.clean_text(initial_text)

        # Generate audio for greeting (None if TTS unavailable — handled gracefully)
        audio_url = self.tts.generate_audio(initial_text)

        session = {
            "id": session_id,
            "user_email": user_email,
            "history": [{"role": "assistant", "content": initial_text}],
            "user_context": {
                "name": name,
                "preferences": preferences,
                "recent_trips_count": len(user_trips)
            },
            "start_time": datetime.now().isoformat(),
        }

        # Persist to disk
        self._save_session(session_id, session)
        logger.info(f"[TravelCoach] Started session {session_id} for {user_email}")

        return {
            "session_id": session_id,
            "text": initial_text,
            "audio_url": audio_url
        }

    def clean_text(self, text: str) -> str:
        """
        Strips markdown symbols to provide clean plain text.
        """
        # Remove bold/italic
        text = re.sub(r'[*_]{1,3}', '', text)
        # Remove headers
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        # Remove table borders and structural symbols
        text = re.sub(r'\|', '', text)
        text = re.sub(r'[-:]{3,}', '', text)
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def process_message(self, session_id: str, text_message: str, file_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Processes user query and returns coach's advice.
        """
        session = self._load_session(session_id)
        if session is None:
            logger.warning(f"[TravelCoach] Session not found: {session_id}")
            raise ValueError(f"Invalid Session: {session_id}")

        if not text_message and not file_data:
            return {"error": "Empty message"}

        # Store text history
        if text_message:
            session["history"].append({"role": "user", "content": text_message})

        # Construct System Prompt with Context
        context = session.get("user_context", {})
        prefs = context.get("preferences", {})
        fav_theme = prefs.get("theme", "General")

        system_prompt = f"""
        You are an enthusiastic and knowledgeable Travel Coach for {context.get('name')}.
        
        User Context:
        - Favorite Travel Theme: {fav_theme}
        - Budget Range: {prefs.get('budget_range', 'Unknown')}
        
        Your Goal:
        1. Inspire the user to travel.
        2. Provide concrete, personalized destination suggestions.
        3. Offer practical tips (visa, best time to visit, packing).
        4. If they ask about their past trips, you can mention they have {context.get('recent_trips_count')} saved trips (but you don't have full details, just the count).
        5. If a file/image is provided, acknowledge it and analyze it in the context of travel planning.
        
        TRIP PLANNING CONVERSATION FLOW:
        - When the user says "plan a trip" or anything similar (e.g. "I want to plan a trip", "help me plan", "let's plan"), 
          respond with EXACTLY: "Which destination would you like to travel to?"
        - When the user then mentions a country, city, or destination name, provide a helpful and detailed trip plan for that place covering:
            * Best time to visit
            * Top 3-5 must-see attractions
            * Local food recommendations
            * Travel tips (visa, currency, transport)
            * Estimated budget range
        - Keep the plan conversational and friendly, not like a rigid list.
        
        IMPORTANT: Use ONLY plain text. DO NOT use Markdown formatting (no bolding with **, no headers with #, no tables, no horizontal rules). Use simple line breaks for separation.
        
        Other Special Instructions:
        - If the user says "best time to visit", ask them which place they have in mind.
        - Always follow up with an offer to help with more details like hotels, day-by-day itinerary, or packing list.
        
        Tone: Friendly, adventurous, professional.
        Keep responses concise and helpful. Use emojis where appropriate.
        """

        # Construct messages for LLM
        is_multimodal = file_data and (
            "image" in file_data.get("content_type", "") or
            "audio" in file_data.get("content_type", "")
        )

        if is_multimodal:
            input_parts = [
                {"text": system_prompt},
                {"text": f"User context: {context}"},
                {"text": "Chat history starts below:"}
            ]
            for msg in session["history"][-5:]:
                input_parts.append({"text": f"{msg['role']}: {msg['content']}"})

            if text_message:
                input_parts.append({"text": f"User says: {text_message}"})

            input_parts.append({
                "inline_data": {
                    "mime_type": file_data["content_type"],
                    "data": file_data["bytes"]
                }
            })

            try:
                ai_text = self.llm.model.generate_content(input_parts).text
            except Exception as e:
                logger.error(f"[TravelCoach] Multimodal LLM Failed: {e}")
                ai_text = "I received your file! Unfortunately, I had a bit of trouble analyzing it in detail. What can I help you with regarding this?"
        else:
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(session["history"][-10:])

            try:
                ai_text = self.llm.generate_response_from_messages(messages)
            except Exception as e:
                logger.error(f"[TravelCoach] LLM Failed: {e}")
                ai_text = "I'm having a bit of trouble connecting to my travel brain. Please try again in a moment."

        # Fallback if empty
        if not ai_text:
            ai_text = "I'm having trouble thinking of a suggestion right now. Could you ask me something else?"

        # Clean text for UI and TTS
        ai_text = self.clean_text(ai_text)

        # Generate audio for AI response (None if TTS unavailable — handled gracefully by frontend)
        audio_url = self.tts.generate_audio(ai_text)

        session["history"].append({"role": "assistant", "content": ai_text})
        # Persist updated session back to disk
        self._save_session(session_id, session)

        return {
            "text": ai_text,
            "audio_url": audio_url,
            "is_completed": False
        }


# Singleton instance
travel_coach = TravelCoach()
