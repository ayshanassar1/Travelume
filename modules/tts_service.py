from gtts import gTTS
import os
import uuid
import time
import logging

logger = logging.getLogger("travelume.tts")

class TTSService:
    def __init__(self, static_dir: str):
        """
        Initializes the TTS service.
        static_dir: Directory where audio files will be saved.
        """
        self.audio_dir = os.path.join(static_dir, "audio")
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

    def generate_audio(self, text: str, lang: str = 'en', retries: int = 3) -> str | None:
        """
        Generates an MP3 file from text and returns the relative URL.
        Retries up to `retries` times with exponential backoff on failure.
        Returns None if all attempts fail (caller must handle gracefully).
        """
        filename = f"chat_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(self.audio_dir, filename)

        for attempt in range(1, retries + 1):
            try:
                tts = gTTS(text=text, lang=lang, slow=False)
                tts.save(filepath)
                logger.info(f"[TTS] Generated audio on attempt {attempt}: {filename}")
                # Return the URL relative to the /static mount
                return f"/static/audio/{filename}"
            except Exception as e:
                wait = 2 ** (attempt - 1)  # 1s, 2s, 4s
                logger.warning(f"[TTS] Attempt {attempt}/{retries} failed: {e}. Retrying in {wait}s...")
                if attempt < retries:
                    time.sleep(wait)

        logger.error(f"[TTS] All {retries} attempts exhausted. Audio will not be available.")
        return None

# The static directory is 'data' at the project root.
# Initialized in travel_coach.py
