import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv(override=True)

# ── API Keys ────────────────────────────────────────────────────────────────
CHATBOT_API_KEY     = os.environ.get("CHATBOT_API_KEY", "")
ITINERARIES_API_KEY = os.environ.get("ITINERARIES_API_KEY", "")

# Model cascade: try best model first, fall back when quota is hit.
# gemma-3-27b-it is confirmed working when Gemini quota is exhausted.
MODEL_CASCADE = [
    "models/gemini-2.0-flash",  # primary (specified)
    "gemini-2.0-flash-lite",    # lighter Gemini
    "gemma-3-27b-it",           # confirmed working fallback
]


class LLMClient:
    """
    Travel Coach LLM client.
    Tries CHATBOT_API_KEY first, then ITINERARIES_API_KEY.
    For each key, tries models in MODEL_CASCADE order.
    gemma-3-27b-it is included as a guaranteed fallback.
    """

    def __init__(self):
        self._keys = [k for k in [CHATBOT_API_KEY, ITINERARIES_API_KEY] if k]
        if not self._keys:
            print("[LLMClient] WARNING: No API key found in environment.")
            self._model_name = None
            self.model = None
            return

        # Configure with primary key + primary model for multimodal use
        genai.configure(api_key=self._keys[0])
        self._model_name = MODEL_CASCADE[0]
        self.model = genai.GenerativeModel(self._model_name)

    # ── Public API ─────────────────────────────────────────────────────────

    def generate_response_from_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Send role/content messages to the AI and return the text reply.
        Cascades through keys and models automatically on quota errors.
        """
        if not self._keys:
            return "The AI assistant is not configured. Please check the API key."

        history: List[Dict] = []
        system_instruction: Optional[str] = None

        for msg in messages:
            role    = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                system_instruction = content
            elif role == "user":
                history.append({"role": "user",  "parts": [content]})
            elif role == "assistant":
                history.append({"role": "model", "parts": [content]})

        if not history or history[-1]["role"] != "user":
            return "Please send a message to get a response."

        # Extract last user message once — reused across all retries
        last_user_message = history.pop()

        # Build attempts: every key × every model in cascade order
        attempts = [
            (key, model)
            for key in self._keys
            for model in MODEL_CASCADE
        ]

        for idx, (api_key, model_name) in enumerate(attempts):
            print(f"[LLMClient] Attempt {idx + 1}: key ending ...{api_key[-6:]}, model={model_name}")
            result = self._call_model(
                api_key=api_key,
                model_name=model_name,
                history=history,
                last_user_message=last_user_message,
                system_instruction=system_instruction,
            )
            if result is not None:
                # Remember which model worked
                self._model_name = model_name
                self.model = genai.GenerativeModel(model_name)
                return result

        return "I'm currently unavailable. Please try again in a few minutes! ✈️"

    # ── Internal ───────────────────────────────────────────────────────────

    def _call_model(
        self,
        api_key: str,
        model_name: str,
        history: List[Dict],
        last_user_message: Dict,
        system_instruction: Optional[str],
    ) -> Optional[str]:
        """
        Single API call attempt. Returns text on success, None on any failure.

        Gemma models do NOT support system_instruction in the constructor —
        for those models we prepend it inside the conversation instead.
        """
        try:
            genai.configure(api_key=api_key)

            is_gemma = "gemma" in model_name.lower()

            if is_gemma:
                # Gemma: embed system instruction as the very first user message
                model = genai.GenerativeModel(model_name)
                adjusted_history = list(history)  # copy
                if system_instruction:
                    # Prepend system prompt as a user/model exchange so the
                    # model respects it without needing system_instruction param
                    sys_turn  = {"role": "user",  "parts": [f"[System Instructions]\n{system_instruction}"]}
                    ack_turn  = {"role": "model", "parts": ["Understood. I will follow these instructions."]}
                    adjusted_history = [sys_turn, ack_turn] + adjusted_history
                chat = model.start_chat(history=adjusted_history)
            else:
                # Gemini: use system_instruction parameter
                model = (
                    genai.GenerativeModel(model_name, system_instruction=system_instruction)
                    if system_instruction
                    else genai.GenerativeModel(model_name)
                )
                chat = model.start_chat(history=history)

            response = chat.send_message(last_user_message["parts"][0])
            return response.text

        except Exception as e:
            err = str(e)
            print(f"[LLMClient]   → Failed ({model_name}): {err[:150]}")
            return None

