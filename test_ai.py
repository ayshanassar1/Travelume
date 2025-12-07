print("Testing Travelume AI...")

try:
    from modules.ai_planner import TravelumeAIPlanner
    print("✅ AI Planner imported")
    
    planner = TravelumeAIPlanner()
    print(f"AI Ready: {planner.use_real_ai}")
    
    # Quick test
    from datetime import datetime
    result = planner._generate_mock_itinerary(
        destination="Dubai",
        days=3,
        budget_range="Mid-range",
        travelers=2,
        travel_style=["Adventure"],
        start_date=datetime.now()
    )
    
    print(f"✅ Test passed! Generated: {result['title']}")
    
except Exception as e:
    print(f"❌ Error: {e}")