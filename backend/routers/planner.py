from fastapi import APIRouter, HTTPException, Depends
import google.generativeai as genai
from datetime import datetime
import os
import sys

from backend.models import AIPlannerForm
from backend.routers.auth import get_current_user

router = APIRouter(
    prefix="/planner",
    tags=["AI Planner"]
)

# Configure Gemini AI for Itinerary Planner
ITINERARIES_API_KEY = os.getenv("ITINERARIES_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=ITINERARIES_API_KEY)
model = genai.GenerativeModel('models/gemini-flash-latest')

@router.post("/generate")
async def generate_itinerary(form: AIPlannerForm, current_user: dict = Depends(get_current_user)):

    try:
        # Calculate days
        start = datetime.fromisoformat(form.start_date)
        end = datetime.fromisoformat(form.end_date)
        days = (end - start).days + 1
        
        # Total budget calculation
        total_budget = form.budget # This is already total budget from frontend logic
        
        # Build prompt for systematic JSON output
        refinement_block = f'ADJUSTMENT: {form.refinement}. Modify plan accordingly.' if form.refinement else ''
        
        prompt = f"""Travel planner: Create a highly detailed and systematic JSON itinerary.
{form.departure_city} → {form.destination}, {start.strftime('%b %d')} to {end.strftime('%b %d, %Y')} ({days}d), Theme:{form.travel_theme}, Pace:{form.travel_pace}, Stay:{form.accommodation_type}, Food:{', '.join(form.food_preferences)}, Transit:{form.travel_mode}, Budget:{form.currency} {total_budget:,} for {form.passengers} pax. {form.additional_prefs or ''}
{refinement_block}

Return ONLY this structured JSON:
{{
  "title": "cinematic and descriptive title",
  "intro": "2-3 sentences providing context and vibe of the trip",
  "budget_disclaimer": "Detailed analysis of whether {form.currency} {total_budget:,} is sufficient for {days} days for {form.passengers} people, mentioning specific high-cost areas like Skydive or 5-star stays if applicable",
  "logistics": [
    {{
      "category": "Nearest Departure Airport",
      "details": "e.g., Cochin International Airport (COK)",
      "cost": "Estimated cost for travel to airport"
    }},
    {{
      "category": "Flight Recommendation",
      "details": "Specific airlines and route details",
      "cost": "Estimated return flight cost for {form.passengers} people"
    }},
    {{
      "category": "Accommodation Recommendation",
      "details": "Specific hotel names and types mentioned in the prompt",
      "cost": "Estimated stay cost for {days} nights"
    }}
  ],
  "itinerary": [
    {{
      "day": 1,
      "date": "Full Date (e.g., January 06, 2026)",
      "theme": "Daily focus/theme",
      "activities": [
        {{
          "time": "Morning (e.g., 8:00 AM)",
          "description": "Detailed activity description",
          "dining": "Breakfast recommendation"
        }},
        {{
          "time": "Afternoon (e.g., 1:00 PM)",
          "description": "Detailed activity description",
          "dining": "Lunch recommendation"
        }},
        {{
          "time": "Evening (e.g., 7:00 PM)",
          "description": "Detailed activity description",
          "dining": "Dinner recommendation"
        }}
      ]
    }}
  ],
  "budget_analysis": {{
    "total_estimated_cost": "Total amount in {form.currency}",
    "breakdown": [
      {{
        "category": "International/Interstate Travel (Flights/Train)",
        "cost": "amt",
        "explanation": "Specific flight or train routes and classes"
      }},
      {{
        "category": "Intercity/Local Transportation",
        "cost": "amt",
        "explanation": "Uber, Private Car, Metro, etc."
      }},
      {{
        "category": "Stay & Accommodation",
        "cost": "amt",
        "explanation": "Daily rate x {days} nights at specific recommended hotels"
      }},
      {{
        "category": "Dining & Local Foodie Experience",
        "cost": "amt",
        "explanation": "Estimated cost for breakfast, lunch, and dinner at recommended spots"
      }},
      {{
        "category": "Activities & Entry Fees",
        "cost": "amt",
        "explanation": "Detailed list of entry fees for museums, parks, or specific tours"
      }},
      {{
        "category": "Miscellaneous & Shopping",
        "cost": "amt",
        "explanation": "Halwa, Souvenirs, etc."
      }}
    ],
    "dining_highlights": [
      {{
        "place": "Name of Iconic Restaurant",
        "dish": "Signature dish to try",
        "vibe": "Quick description of why it's a must-visit"
      }}
    ],
    "saving_tips": ["Actionable tip 1", "Actionable tip 2", "Actionable tip 3"]
  }}
}}

Generate exactly {days} day entries. Be hyper-specific with real places, restaurants, and local gems. No markdown wrapping."""
        
        response = model.generate_content(prompt)
        import json
        try:
            # Clean response text in case of markdown wrapping or extra text
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            itinerary_json = json.loads(clean_text)
            return {"itinerary": itinerary_json, "is_raw": False}
        except:
            # Fallback if AI fails to return clean JSON
            return {"itinerary": response.text, "is_raw": True}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
