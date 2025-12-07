"""
AI Travel Planner Module for Travelume
Integrated with Database for persistent storage
"""

import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import json
import os
import time

# ==================== DATABASE INTEGRATION ====================
try:
    from modules.database import get_database
    DATABASE_AVAILABLE = True
except ImportError as e:
    DATABASE_AVAILABLE = False
    st.warning(f"⚠️ Database module not available: {e}. Trips will be saved locally only.")

# ==================== FIX FOR WHITE TEXT ====================
st.markdown("""
<style>
    /* NUCLEAR FIX: MAKE EVERYTHING BLACK ON WHITE */
    
    /* 1. Force ALL text to be BLACK */
    * {
        color: #000000 !important;
    }
    
    /* 2. Force ALL backgrounds WHITE */
    body, .stApp, main, [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    
    /* 3. Force ALL Streamlit text BLACK */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #000000 !important;
    }
    
    /* 4. Force input fields to have BLACK text */
    .stTextInput input, .stTextArea textarea, .stSelectbox select,
    .stDateInput input, .stNumberInput input, .stMultiSelect input {
        color: #000000 !important;
        background-color: white !important;
        border: 1px solid #cccccc !important;
    }
    
    /* 5. Make labels DARK BLUE and BOLD */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stSlider label, .stDateInput label, .stCheckbox label,
    .stRadio label, .stNumberInput label, .stMultiSelect label {
        color: #1a237e !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* 6. Make containers white with borders */
    .stContainer, .element-container, .block-container {
        background-color: white !important;
    }
    
    /* 7. Force buttons to work normally */
    .stButton button {
        color: white !important;
        background-color: #1a237e !important;
        cursor: pointer !important;
    }
    
    /* 8. Custom progress bar */
    .stProgress > div > div > div > div {
        background-color: #1a237e !important;
    }
    
    /* 9. Simple card styling */
    .custom-card {
        background-color: white !important;
        border: 2px solid #1a237e !important;
        border-radius: 15px !important;
        padding: 25px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    /* 10. Force enable ALL buttons */
    button {
        pointer-events: auto !important;
        opacity: 1 !important;
        cursor: pointer !important;
    }
    
    /* 11. Remove disabled button styling */
    button[disabled] {
        opacity: 1 !important;
        background-color: #1a237e !important;
    }
    
    /* FIX FOR ALL ITINERARY TEXT - Make ALL AI response text BLACK */
    .stMarkdown p, .stMarkdown div, .stMarkdown span, .stMarkdown li, 
    .stMarkdown strong, .stMarkdown em, .stMarkdown h1, .stMarkdown h2, 
    .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .stMarkdown code, .stMarkdown pre {
        color: #000000 !important;
    }
    
    /* Target ALL tab content where itinerary is displayed */
    [data-testid="stTabContent"] p, 
    [data-testid="stTabContent"] div, 
    [data-testid="stTabContent"] span,
    [data-testid="stTabContent"] li,
    [data-testid="stTabContent"] strong,
    [data-testid="stTabContent"] em,
    [data-testid="stTabContent"] h3,
    [data-testid="stTabContent"] code,
    [data-testid="stTabContent"] pre {
        color: #000000 !important;
    }
    
    /* Force bullet points and list items black */
    .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
        color: #000000 !important;
    }
    
    /* Make the daily plan tab text black */
    .stTabs [data-baseweb="tab-panel"] * {
        color: #000000 !important;
    }
    
    /* Database status badge */
    .db-status {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 10px;
    }
    .db-connected {
        background-color: #d4edda;
        color: #155724;
    }
    .db-disconnected {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# ==================== API CONFIGURATION ====================
# Get API key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

# Configure Gemini AI
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-flash-latest')
        AI_ENABLED = True
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        AI_ENABLED = False
else:
    AI_ENABLED = False

def render_ai_planner():
    """Main AI travel planner function with detailed questions."""
    
    # Initialize session state for button
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    
    # Show database connection status
    db_status_html = ""
    if DATABASE_AVAILABLE:
        db_status_html = '<span class="db-status db-connected">✅ Database Connected</span>'
    else:
        db_status_html = '<span class="db-status db-disconnected">⚠️ Database Offline</span>'
    
    st.markdown(
    f"<h1 style='color: black;'>✈️ AI Travel Itinerary Planner {db_status_html}</h1>",
    unsafe_allow_html=True)
    
    st.markdown(
    "<h3 style='color: black;'>Get a personalized travel plan tailored just for you!</h3>",
    unsafe_allow_html=True)
    
    # Show warning if AI is not available
    if not AI_ENABLED:
        st.warning("""
        ⚠️ **AI Features Disabled**  
        Gemini API key is not configured. To enable AI itinerary generation:
        
        1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a `.streamlit/secrets.toml` file
        3. Add: `GOOGLE_API_KEY = "your-api-key-here"`
        
        Meanwhile, you can use sample itineraries below.
        """)
        
        show_sample_itineraries()
        return
    
    # Show login prompt if not authenticated
    if not st.session_state.get("authenticated", False):
        st.info("🔐 **Tip:** Login to save your trips to your account and access them from any device!")
    
    # Progress bar
    st.markdown(
    "<h3 style='color: black;'>📋 Tell us about your dream trip</h3>",
    unsafe_allow_html=True)

    progress = st.progress(0)
    
    # ==================== STEP 1: BASIC INFO ====================
    with st.container(border=True):
        st.markdown(
    "<h4 style='color: black;'>📍 <b>Step 1: Basic Information</b></h4>",
    unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>1. Where are you starting your trip from?</p>",
                unsafe_allow_html=True)
            departure_city = st.text_input(
                "",placeholder="e.g., Mumbai, Delhi, Bangalore",
                help="Your starting city or airport",
                key="departure_city")
        
        with col2:
            st.markdown(
                "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>2. Search for your destination country/city</p>",
                unsafe_allow_html=True)
    
            destination = st.text_input(
                "",placeholder="e.g., Dubai, Bali, Paris",
                help="Where do you want to go?",
                key="destination")
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(
                "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>3. Select Start Date</p>",
                unsafe_allow_html=True)
            start_date = st.date_input(
                "",min_value=datetime.today(),
                value=datetime.today() + timedelta(days=30),
                key="start_date")

        with col4:
            st.markdown(
                "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>4. Select End Date</p>",
                unsafe_allow_html=True)
            end_date = st.date_input(
                "",min_value=datetime.today() + timedelta(days=1),
                value=datetime.today() + timedelta(days=37),
                key="end_date")
        
        # Calculate days
        if start_date and end_date:
            days = (end_date - start_date).days
            if days > 0:
                st.info(f"🕐 **Trip Duration:** {days} days")
            else:
                st.error("End date must be after start date!")
    
    progress.progress(20)
    
    # ==================== STEP 2: TRAVEL PREFERENCES ====================
    with st.container(border=True):
        st.markdown("<h4 style='color:black;'>🎯 <b>Step 2: Travel Preferences</b></h4>",unsafe_allow_html=True)

        
        st.markdown(
    "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>5. Which of these travel themes best describes your dream getaway?</p>",
    unsafe_allow_html=True)

        travel_theme = st.selectbox(
            "",
            [
                "Beach & Relaxation 🏖️",
                "Adventure & Sports ⛰️",
                "Cultural & Historical 🏛️",
                "Food & Culinary 🍽️",
                "Shopping & Luxury 🛍️",
                "Nature & Wildlife 🦒",
                "Romantic Getaway 💖",
                "Family Fun 👨‍👩‍👧‍👦",
                "Party & Nightlife 🎉",
                "Wellness & Spa 🧘‍♀️"
            ],
            index=0,
            key="travel_theme")
        
        st.markdown(
    "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>6. What pace of travel do you prefer?</p>",
    unsafe_allow_html=True)

        travel_pace = st.selectbox(
            "",
                [
                    "Relaxed (Plenty of downtime)",
                    "Moderate (Mix of activities and rest)",
                    "Fast-paced (See as much as possible)",
                    "Flexible (Go with the flow)"
                ],
                index=1,
                key="travel_pace")


        
        st.markdown(
    "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>7. What kind of weather do you prefer for your trip?</p>",
    unsafe_allow_html=True)

        weather_preference = st.selectbox(
            "",
                [
                    "Warm & Sunny ☀️",
                    "Cool & Pleasant 🌤️",
                    "Cold & Snowy ❄️",
                    "Any weather is fine 🌈",
                    "Avoid rainy season ☔"
                ],
                index=0,
                key="weather_preference")

    
    progress.progress(40)
    
    # ==================== STEP 3: ACCOMMODATION & FOOD ====================
    with st.container(border=True):
        st.markdown("<h4 style='color:black;'>🏨 <b>Step 3: Accommodation & Dining</b></h4>",unsafe_allow_html=True)
        
        st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>8. What type of accommodation would you prefer?</p>",unsafe_allow_html=True)

        accommodation_type = st.selectbox(
            "",
                [
                    "Luxury Hotels (5-star) ⭐⭐⭐⭐⭐",
                    "Boutique Hotels 🏨",
                    "Budget Hotels/Hostels 🏠",
                    "Vacation Rentals (Airbnb) 🏡",
                    "Resorts & Spas 🌴",
                    "Homestays & B&Bs 🛌"
                ],
                index=0,
                key="accommodation_type")
        
        st.markdown(
        "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>9. What type of food would you like to enjoy during your trip?</p>",unsafe_allow_html=True)

        food_preferences = st.multiselect(
            "",
                [
                    "Local Street Food 🍢",
                    "Fine Dining 🍽️",
                    "Vegetarian/Vegan 🥗",
                    "Seafood Specialties 🦞",
                    "International Cuisine 🌍",
                    "Cooking Classes 👨‍🍳",
                    "Food Tours 🚶‍♀️"
                ],
                default=["Local Street Food 🍢", "Fine Dining 🍽️"],
                key="food_preferences")

    
    progress.progress(60)
    
    # ==================== STEP 4: TRANSPORT & BUDGET ====================
    with st.container(border=True):
        st.markdown("<h4 style='color:black;'>💰 <b>Step 4: Transport & Budget</b></h4>",unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>10. How would you like to travel from departure to destination?</p>",unsafe_allow_html=True)
            travel_mode = st.selectbox(
                "",
                [
                    "Direct Flight ✈️",
                    "Flight with Stopover 🛫",
                    "Train Journey 🚆",
                    "Road Trip 🚗",
                    "Cruise Ship 🚢",
                    "Most Economical Option 💸"
                ],
                index=0,
                key="travel_mode")

            st.markdown(
            "<p style='color:black; font-size:16px; font-weight:500; margin:0;'>11. Which currency would you like to use for your trip?</p>",unsafe_allow_html=True)
            currency = st.selectbox(
                "",
                    [
                        "INR (Indian Rupees)",
                        "USD (US Dollars)", 
                        "EUR (Euros)",
                        "Local Currency"
                    ],
                    index=0,
                    key="currency")

        with col6:
            st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>12. What is your estimated travel budget per person? (INR)</p>",unsafe_allow_html=True)
    
            budget = st.slider(
                "",
                    min_value=5000,
                    max_value=500000,
                    value=50000,
                    step=5000,
                    help="Select your total budget including flights, accommodation, food, and activities",
                    key="budget")
           
            st.markdown(f"<p style='color:black; font-weight:bold;'>Selected Budget: ₹{budget:,}</p>",unsafe_allow_html=True)
            
            st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>13. How many passengers?</p>",unsafe_allow_html=True)

            passengers = st.number_input(
                "",min_value=1,
                max_value=20,
                value=2,
                step=1,
                key="passengers")
            
            total_budget = budget * passengers
            st.markdown(f"<p style='color:black; font-weight:bold;'>Total Budget ({passengers} people): ₹{total_budget:,}</p>",unsafe_allow_html=True)

    
    progress.progress(80)
    
    # ==================== STEP 5: ADDITIONAL PREFERENCES ====================
    with st.container(border=True):
        st.markdown(f"<p style='color:black; font-weight:bold;'>Total Budget ({passengers} people): ₹{total_budget:,}</p>",unsafe_allow_html=True)
        
        st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>14. Any additional preferences or specific places/activities you'd like to include?</p>",unsafe_allow_html=True)

        additional_prefs = st.text_area(
            "",
                placeholder="e.g., Must visit Eiffel Tower, love beach activities, dietary restrictions, special occasions...",
                height=100,
                help="The more details you provide, the better your personalized itinerary will be!",
                key="additional_prefs")

    
    progress.progress(100)
    
    # ==================== DEBUG INFO ====================
    with st.expander("🔧 Debug Information", expanded=False):
        st.write("**Field Status:**")
        st.write(f"- Departure City: '{departure_city}' (Length: {len(departure_city.strip())})")
        st.write(f"- Destination: '{destination}' (Length: {len(destination.strip())})")
        st.write(f"- Both filled: {bool(departure_city.strip() and destination.strip())}")
        st.write(f"- API Enabled: {AI_ENABLED}")
        st.write(f"- Database Available: {DATABASE_AVAILABLE}")
        st.write(f"- User Authenticated: {st.session_state.get('authenticated', False)}")
        if st.session_state.get('authenticated', False):
            st.write(f"- Current User: {st.session_state.current_user.get('email', 'Unknown')}")
    
    # ==================== GENERATE BUTTON ====================
    st.markdown("---")
    st.markdown("<h3 style='color:black; text-align:center;'>Ready to Generate Your Itinerary!</h3>", unsafe_allow_html=True)
    
    col_gen1, col_gen2, col_gen3 = st.columns([1, 2, 1])
    
    with col_gen2:
        # ALWAYS ENABLE THE BUTTON - validation will happen after click
        generate_clicked = st.button(
            "✨ **GENERATE PERSONALIZED ITINERARY**",
            use_container_width=True,
            type="primary"
        )
    
    # ==================== GENERATE ITINERARY ====================
    if generate_clicked or st.session_state.button_clicked:
        st.session_state.button_clicked = True
        
        # Validation checks
        errors = []
        
        # Check required fields
        if not departure_city.strip():
            errors.append("Please enter departure city")
        if not destination.strip():
            errors.append("Please enter destination")
        
        # Check dates
        if start_date and end_date:
            days = (end_date - start_date).days
            if days <= 0:
                errors.append("End date must be after start date")
        
        # Show errors if any
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            st.session_state.button_clicked = False
            return
        
        # Check API
        if not AI_ENABLED:
            st.error("❌ AI features are disabled. Please configure API key.")
            st.session_state.button_clicked = False
            return
        
        # All checks passed - generate itinerary
        with st.spinner("🤖 AI is creating your perfect personalized itinerary..."):
            try:
                # Build detailed prompt
                prompt = f"""
                Create a detailed {days}-day personalized travel itinerary from {departure_city} to {destination}.
                
                TRAVELER PROFILE:
                - Departure From: {departure_city}
                - Destination: {destination}
                - Travel Dates: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')} ({days} days)
                - Travel Theme: {travel_theme}
                - Travel Pace: {travel_pace}
                - Weather Preference: {weather_preference}
                - Accommodation: {accommodation_type}
                - Food Preferences: {', '.join(food_preferences)}
                - Travel Mode: {travel_mode}
                - Currency: {currency}
                - Budget: ₹{budget:,} per person (Total: ₹{total_budget:,} for {passengers} people)
                {f"- Additional Preferences: {additional_prefs}" if additional_prefs else ""}
                
                CREATE A COMPREHENSIVE ITINERARY INCLUDING:
                
                1. **DAY-BY-DAY SCHEDULE** (Morning/Afternoon/Evening for each day)
                2. **FLIGHT/TRANSPORT DETAILS** from {departure_city} to {destination}
                3. **ACCOMMODATION RECOMMENDATIONS** matching the selected type
                4. **FOOD & DINING** suggestions based on preferences
                5. **ACTIVITIES & SIGHTSEEING** aligned with travel theme
                6. **DAILY BUDGET BREAKDOWN** (Accommodation, Food, Activities, Transport)
                7. **PACKING TIPS** considering weather and activities
                8. **LOCAL TIPS** (Currency, Language, Etiquette, Safety)
                9. **TOTAL COST ESTIMATE** within the specified budget
                
                Format with emojis, clear sections, and practical advice. Make it engaging and personalized!
                """
                
                # Generate itinerary
                response = model.generate_content(prompt)
                itinerary = response.text
                
                # Display the itinerary
                display_itinerary(
                    itinerary, destination, days, budget, total_budget, passengers,
                    departure_city, start_date, end_date, travel_theme, travel_mode
                )
                
            except Exception as e:
                st.error(f"❌ Error generating itinerary: {str(e)}")
                st.info("💡 Try again or check your API key configuration.")
                st.session_state.button_clicked = False

def display_itinerary(itinerary, destination, days, budget, total_budget, passengers,
                      departure_city, start_date, end_date, travel_theme, travel_mode):
    """Display the generated personalized itinerary."""
    
    st.success(f"✅ **Personalized {days}-Day Itinerary Generated!**")
    st.balloons()
    
    # Trip summary card
    with st.container(border=True):
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        
        with col_sum1:
            st.markdown(f"<p style='color:black; margin:0;'><b>📍 From:</b> {departure_city}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:black; margin:0;'><b>✈️ To:</b> {destination}</p>", unsafe_allow_html=True)

        with col_sum2:
            st.markdown(f"<p style='color:black; margin:0;'><b>📅 Dates:</b> {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:black; margin:0;'><b>👥 Travelers:</b> {passengers}</p>", unsafe_allow_html=True)

        with col_sum3:
            st.markdown(f"<p style='color:black; margin:0;'><b>💰 Budget per person:</b> ₹{budget:,}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:black; margin:0;'><b>💰 Total budget:</b> ₹{total_budget:,}</p>", unsafe_allow_html=True)

    
    # Display itinerary in tabs
    # Custom CSS to make tab labels black
    st.markdown("""<style>/* Tab label text color */div[class*="css-"] > button[role="tab"] {color: black !important;}</style>""",unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Full Itinerary", "🗓️ Daily Plan", "💾 Save Trip"])
   
    with tab1:
        st.markdown( f"<h2 style='color:black;'>✨ Your Personalized {destination} Itinerary</h2>",unsafe_allow_html=True)
        st.divider()
        
        # Display the AI response with BLACK TEXT
        st.markdown(f"""
        <div style="color: black; background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        {itinerary}
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f"<h3 style='color:black;'>🗓️ Daily Schedule Overview</h3>", unsafe_allow_html=True)
        
        # Simple parsing for daily highlights
        lines = itinerary.split('\n')
        day_count = 1
        
        # Create a container with black text for the daily plan
        st.markdown("""
        <div style="color: black; background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">
        """, unsafe_allow_html=True)
        
        for line in lines:
            if 'day' in line.lower() and ('1' in line or '2' in line or '3' in line or '4' in line or '5' in line):
                st.markdown(f"<h4 style='color:black;'>📍 {line}</h4>", unsafe_allow_html=True)
                day_count += 1
            elif 'morning:' in line.lower() or 'afternoon:' in line.lower() or 'evening:' in line.lower():
                st.markdown(f"<p style='color:black; font-weight:bold; margin:5px 0;'>{line}</p>", unsafe_allow_html=True)
            elif line.strip() and len(line.strip()) > 20:
                st.markdown(f"<p style='color:black; margin:5px 0 5px 20px;'>• {line.strip()}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown(f"<h3 style='color:black;'>💾 Save Your Personalized Trip</h3>", unsafe_allow_html=True)
        
        # Show database status
        if DATABASE_AVAILABLE:
            if st.session_state.get("authenticated", False):
                st.success("✅ Your trip will be saved to your account database")
            else:
                st.info("🔐 **Login to save to your account** - Your trip will be saved locally for now")
        else:
            st.warning("⚠️ Database offline - Trip will be saved locally only")
        
        with st.form(key="save_form"):
            # Trip Name
            st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>Trip Name</p>",unsafe_allow_html=True)
            trip_name = st.text_input(
                "",
                value=f"{destination} Trip - {days} Days ({start_date.strftime('%b %Y')})",
                key="trip_name")
    
            # Additional Notes
            st.markdown("<p style='color:black; font-size:16px; font-weight:500; margin:0;'>Additional Notes</p>",unsafe_allow_html=True)
            trip_notes = st.text_area(
                "",
                placeholder="Add personal notes or reminders...",
                height=80,
                key="trip_notes")
            
            save_col1, save_col2 = st.columns([1, 1])
            
            with save_col1:
                save_button = st.form_submit_button(
                    "💾 Save Trip",
                    use_container_width=True
                )
            
            with save_col2:
                share_button = st.form_submit_button(
                    "📤 Share Itinerary",
                    use_container_width=True
                )
            
            if save_button:
                if not trip_name.strip():
                    st.error("Please enter a trip name")
                else:
                    if save_trip_data(
                        name=trip_name,
                        departure_city=departure_city,
                        destination=destination,
                        days=days,
                        budget=budget,
                        total_budget=total_budget,
                        passengers=passengers,
                        itinerary=itinerary,
                        notes=trip_notes,
                        start_date=start_date.isoformat(),
                        end_date=end_date.isoformat(),
                        travel_theme=travel_theme,
                        travel_mode=travel_mode
                    ):
                        # Success message already shown in save_trip_data
                        pass
            
            if share_button:
                st.info("📧 Share feature coming in next update!")
        
        st.divider()
        if st.button("🔄 Create Another Itinerary", use_container_width=True):
            st.session_state.button_clicked = False
            st.rerun()

def save_trip_data(name, departure_city, destination, days, budget, total_budget,
                   passengers, itinerary, notes, start_date, end_date, 
                   travel_theme=None, travel_mode=None):
    """Save trip data to database AND local file."""
    
    # Create trip data structure
    trip_data = {
        "name": name,
        "departure_city": departure_city,
        "destination": destination,
        "duration_days": days,
        "budget_per_person": budget,
        "total_budget": total_budget,
        "passengers": passengers,
        "itinerary": itinerary,
        "notes": notes,
        "start_date": start_date,
        "end_date": end_date,
        "travel_theme": travel_theme,
        "travel_mode": travel_mode,
        "status": "saved",
        "type": "ai_generated",
        "ai_generated": True,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_success = False
    saved_to_db = False
    db_message = ""
    
    # ==================== SAVE TO DATABASE (IF AVAILABLE & USER LOGGED IN) ====================
    if DATABASE_AVAILABLE and st.session_state.get("authenticated", False):
        try:
            db = get_database()
            user_email = st.session_state.current_user["email"]
            trip_id = db.save_ai_trip(user_email, trip_data)
            
            if trip_id:
                saved_to_db = True
                save_success = True
                db_message = f"✅ '{name}' saved to your account database!"
                
                # Show database info
                user_trips = db.get_user_trips(user_email)
                st.success(f"{db_message} (You have {len(user_trips)} saved trips)")
        except Exception as e:
            db_message = f"⚠️ Could not save to database: {str(e)}. Saving locally instead."
            st.warning(db_message)
    
    # ==================== ALWAYS SAVE LOCALLY AS BACKUP ====================
    try:
        os.makedirs("data/trips", exist_ok=True)
        
        # Add metadata for local save
        local_trip_data = trip_data.copy()
        local_trip_data["id"] = datetime.now().strftime("%Y%m%d%H%M%S")
        local_trip_data["created_at"] = datetime.now().isoformat()
        
        # Add user info if available
        if st.session_state.get("authenticated", False):
            local_trip_data["user_email"] = st.session_state.current_user["email"]
        else:
            local_trip_data["user_email"] = "guest"
        
        # Save to file
        filename = f"data/trips/trip_{local_trip_data['id']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(local_trip_data, f, indent=4, ensure_ascii=False)
        
        # Update session state
        if "saved_trips" not in st.session_state:
            st.session_state.saved_trips = []
        
        # Check if trip already exists
        existing_ids = [t.get("id") for t in st.session_state.saved_trips]
        if local_trip_data["id"] not in existing_ids:
            st.session_state.saved_trips.append(local_trip_data)
        
        if not saved_to_db:
            save_success = True
            if st.session_state.get("authenticated", False):
                st.success(f"✅ '{name}' saved locally! (Database unavailable)")
            else:
                st.success(f"✅ '{name}' saved locally! Login to save to your account.")
                
    except Exception as e:
        st.error(f"❌ Local save error: {str(e)}")
        return False
    
    # ==================== SHOW SAVE LOCATION ====================
    if save_success:
        # Show where trip was saved
        col1, col2 = st.columns(2)
        with col1:
            if saved_to_db:
                st.info("📍 **Saved to:** Account Database")
            else:
                st.info("📍 **Saved to:** Local Storage")
        
        with col2:
            # Show quick actions
            if st.button("📁 View My Trips", key="view_trips_btn"):
                if st.session_state.get("authenticated", False):
                    st.session_state.current_page = 'account'
                    st.rerun()
                else:
                    st.info("Login to view your trips in your account")
    
    return save_success

def show_sample_itineraries():
    """Show sample itineraries when AI is disabled."""
    st.subheader("📚 Sample Itineraries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("##### 🌴 Bali Getaway")
            st.write("**8 Days • ₹45,000/person**")
            st.write("• Ubud cultural tour")
            st.write("• Beach relaxation")
            st.write("• Temple visits")
            st.write("• Local cuisine")
    
    with col2:
        with st.container(border=True):
            st.markdown("##### 🏙️ Dubai Luxury")
            st.write("**5 Days • ₹75,000/person**")
            st.write("• Burj Khalifa visit")
            st.write("• Desert safari")
            st.write("• Shopping spree")
            st.write("• Fine dining")
    
    with col3:
        with st.container(border=True):
            st.markdown("##### 🗼 Paris Romance")
            st.write("**7 Days • ₹60,000/person**")
            st.write("• Eiffel Tower")
            st.write("• Louvre Museum")
            st.write("• Seine River cruise")
            st.write("• French cuisine")

# Add emergency test button at the bottom
st.markdown("---")
if st.button("🚨 Emergency Test: Check Database Connection", type="secondary"):
    if DATABASE_AVAILABLE:
        try:
            db = get_database()
            stats = db.get_statistics()
            st.success(f"✅ Database connected! Stats: {stats['total_users']} users, {stats['total_trips']} trips")
        except Exception as e:
            st.error(f"❌ Database error: {str(e)}")
    else:
        st.error("❌ Database module not available")

# Run the app
if __name__ == "__main__":
    render_ai_planner()