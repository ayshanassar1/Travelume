"""
Travelume - AI Travel Planner
Main Application File
"""

import streamlit as st
import re
import webbrowser
import os
import json
from datetime import datetime, date
from modules.hotel_booking import show_hotel_booking_page, integrate_hotels_with_itinerary
from modules.agency_ui import show_agency_directory
from modules.journal import JournalManager
from modules.flight_booking import show_flight_booking_page, integrate_flights_with_itinerary
from modules.chatbot_ui import render_chatbot_sidebar, render_chatbot_popover

# ---- Custom CSS for White Button ----
custom_css = """
<style>
div.stButton > button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #ddd !important;
    border-radius: 6px !important;
}
div.stButton > button:hover {
    background-color: #f5f5f5 !important;
    border: 1px solid #bbb !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Configure page
st.set_page_config(
    page_title="Travelume - AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'users' not in st.session_state:
    # Load users from file if exists, otherwise initialize empty
    try:
        with open('users.json', 'r') as f:
            st.session_state.users = json.load(f)
    except FileNotFoundError:
        st.session_state.users = {}
if 'saved_trips' not in st.session_state:
    # Initialize empty saved trips structure
    st.session_state.saved_trips = {}
if 'account_tab' not in st.session_state:
    st.session_state.account_tab = "profile"
if 'journal_action' not in st.session_state:
    st.session_state.journal_action = None
if 'current_journal' not in st.session_state:
    st.session_state.current_journal = None

# Create journals directory structure
import os
from pathlib import Path
journals_dir = Path("data/journals")
journals_dir.mkdir(exist_ok=True, parents=True)
(journals_dir / "images").mkdir(exist_ok=True, parents=True)
(journals_dir / "pdfs").mkdir(exist_ok=True, parents=True)

def save_users():
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(st.session_state.users, f, indent=2)

def save_trips():
    """Save trips to JSON file"""
    with open('saved_trips.json', 'w') as f:
        json.dump(st.session_state.saved_trips, f, indent=2)

def load_trips():
    """Load trips from JSON file with error handling"""
    try:
        with open('saved_trips.json', 'r') as f:
            data = json.load(f)
            # Ensure data is properly formatted
            if isinstance(data, dict):
                # Check each user's trips to ensure they're lists
                for user_email, trips in data.items():
                    if not isinstance(trips, list):
                        data[user_email] = []
                return data
            else:
                # If file is not a dict, return empty dict
                return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

# ==================== SAVED TRIPS FUNCTIONS ====================
def save_current_trip(trip_name, destination, duration, budget, itinerary_data=None):
    """Save a trip for the current user"""
    if not st.session_state.authenticated:
        st.error("Please login to save trips!")
        return False
    
    user_email = st.session_state.current_user['email']
    
    # Load fresh trips data to avoid corruption
    st.session_state.saved_trips = load_trips()
    
    # Ensure user's saved trips exists as a list
    if user_email not in st.session_state.saved_trips:
        st.session_state.saved_trips[user_email] = []
    elif not isinstance(st.session_state.saved_trips[user_email], list):
        # Convert to list if it's not a list
        st.session_state.saved_trips[user_email] = []
    
    # Check if trip with same name already exists
    for trip in st.session_state.saved_trips[user_email]:
        if trip['name'].lower() == trip_name.lower():
            st.error(f"A trip named '{trip_name}' already exists!")
            return False
    
    new_trip = {
        'id': str(int(datetime.now().timestamp())),  # Unique ID
        'name': trip_name,
        'destination': destination,
        'duration': duration,
        'budget': budget,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'itinerary_data': itinerary_data or {}
    }
    
    st.session_state.saved_trips[user_email].append(new_trip)
    save_trips()
    
    # Get current count of trips
    trip_count = len(st.session_state.saved_trips[user_email])
    st.success(f"✅ '{trip_name}' saved to your account! (You have {trip_count} saved trip{'s' if trip_count != 1 else ''})")
    return True

def delete_saved_trip(trip_id):
    """Delete a saved trip"""
    if not st.session_state.authenticated:
        return False
    
    user_email = st.session_state.current_user['email']
    
    # Load fresh trips data
    st.session_state.saved_trips = load_trips()
    
    if user_email in st.session_state.saved_trips:
        # Find and remove the trip
        for i, trip in enumerate(st.session_state.saved_trips[user_email]):
            if trip['id'] == trip_id:
                trip_name = trip['name']
                st.session_state.saved_trips[user_email].pop(i)
                save_trips()
                st.success(f"Trip '{trip_name}' deleted successfully!")
                return True
    
    return False

def get_user_saved_trips():
    """Get saved trips for current user"""
    if not st.session_state.authenticated:
        return []
    
    user_email = st.session_state.current_user['email']
    
    # Load fresh trips data
    st.session_state.saved_trips = load_trips()
    
    trips = st.session_state.saved_trips.get(user_email, [])
    
    # Ensure trips is a list
    if not isinstance(trips, list):
        trips = []
        st.session_state.saved_trips[user_email] = trips
        save_trips()
    
    return trips

def show_saved_trips_section():
    """Display saved trips in the account page"""
    st.markdown("---")
    st.markdown("### 💼 My Saved Trips")
    
    saved_trips = get_user_saved_trips()
    
    if not saved_trips:
        st.info("📭 You haven't saved any trips yet. Create a trip using our AI Planner or browse destinations to save!")
        st.markdown("---")
        # Show quick links to destinations
        st.markdown("**💡 Quick ways to save trips:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🌍 Browse Destinations", use_container_width=True):
                st.session_state.current_page = 'destinations'
                st.rerun()
        with col2:
            if st.button("🤖 Try AI Planner", use_container_width=True):
                st.session_state.current_page = 'ai_planner'
                st.rerun()
        with col3:
            if st.button("✈️ View Dubai", use_container_width=True):
                st.session_state.current_page = 'dubai_plan'
                st.rerun()
        return
    
    # Display number of trips
    st.success(f"✅ You have {len(saved_trips)} saved trip{'s' if len(saved_trips) != 1 else ''}")
    
    # Display trips in a grid
    cols = st.columns(2)
    
    for idx, trip in enumerate(saved_trips):
        with cols[idx % 2]:
            with st.container(border=True, height=280):
                # Trip header with delete button
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {trip['name']}")
                with col2:
                    if st.button("🗑️", key=f"delete_{trip['id']}", help="Delete trip"):
                        if delete_saved_trip(trip['id']):
                            st.rerun()
                
                # Trip details
                st.markdown(f"**📍 Destination:** {trip['destination']}")
                st.markdown(f"**📅 Duration:** {trip['duration']}")
                st.markdown(f"**💰 Budget:** {trip['budget']}")
                st.markdown(f"**📅 Saved on:** {trip['created_at'].split()[0]}")
                
                # View trip button
                if st.button("📋 View Details", key=f"view_{trip['id']}", use_container_width=True):
                    show_trip_details(trip)

def show_trip_details(trip):
    """Show detailed view of a saved trip"""
    st.markdown(f"#### 📋 {trip['name']}")
    
    # Basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**📍 Destination:**  \n{trip['destination']}")
    with col2:
        st.markdown(f"**📅 Duration:**  \n{trip['duration']}")
    with col3:
        st.markdown(f"**💰 Budget:**  \n{trip['budget']}")
    
    st.markdown(f"**📅 Created:** {trip['created_at']}")
    st.markdown(f"**🔄 Last Updated:** {trip['updated_at']}")
    
    # Show itinerary data if available
    if trip.get('itinerary_data') and isinstance(trip['itinerary_data'], dict) and trip['itinerary_data']:
        st.markdown("---")
        st.markdown("#### 📝 Itinerary Details")
        
        itinerary = trip['itinerary_data']
        
        if 'highlights' in itinerary and itinerary['highlights']:
            st.markdown("**✨ Highlights:**")
            for highlight in itinerary['highlights']:
                st.markdown(f"- {highlight}")
        
        if 'day_plans' in itinerary and itinerary['day_plans']:
            st.markdown("**🗓️ Daily Plans:**")
            for day_plan in itinerary['day_plans']:
                with st.expander(f"{day_plan.get('day', 'Day')}: {day_plan.get('title', 'Activities')}"):
                    activities = day_plan.get('activities', [])
                    if activities:
                        for activity in activities:
                            st.markdown(f"• {activity}")
                    else:
                        st.info("No activities listed for this day")
        
        if 'budget_breakdown' in itinerary and itinerary['budget_breakdown']:
            st.markdown("**💰 Budget Breakdown:**")
            for item, amount in itinerary['budget_breakdown'].items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"{item}")
                with col2:
                    st.markdown(f"**{amount}**")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Edit Trip Name", use_container_width=True):
            # Simple edit name functionality
            new_name = st.text_input("New Trip Name", value=trip['name'], key=f"edit_{trip['id']}")
            if st.button("Save Name", key=f"save_name_{trip['id']}"):
                if new_name and new_name != trip['name']:
                    # Update trip name
                    user_email = st.session_state.current_user['email']
                    # Load fresh data
                    st.session_state.saved_trips = load_trips()
                    for t in st.session_state.saved_trips[user_email]:
                        if t['id'] == trip['id']:
                            t['name'] = new_name
                            t['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            save_trips()
                            st.success(f"Trip renamed to '{new_name}'!")
                            st.rerun()
                            break
    with col2:
        # Button to create journal from this trip
        if st.button("📝 Create Journal", key=f"journal_trip_{trip['id']}", use_container_width=True):
            st.session_state.account_tab = "my_journals"
            st.session_state.journal_action = "create"
            st.session_state.linked_trip_id = trip['id']
            st.session_state.current_page = 'account'
            st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("← Back to My Trips", key=f"back_from_{trip['id']}"):
        st.rerun()

# ==================== ADDED: AUTHENTICATION FUNCTIONS ====================
def show_auth_page():
    """Show login/signup page"""
    # Tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn", type="primary"):
            if login_email and login_password:
                # Check if user exists
                if login_email in st.session_state.users:
                    user_data = st.session_state.users[login_email]
                    # Simple password check (in real app, use hashing!)
                    if user_data['password'] == login_password:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user_data
                        st.session_state.current_page = 'home'
                        st.success(f"Welcome back, {user_data['name']}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password!")
                else:
                    st.error("Email not registered!")
            else:
                st.warning("Please enter email and password")
    
    with tab2:
        st.markdown("### Create New Account")
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Create Account", key="signup_btn", type="primary"):
            if not signup_name:
                st.error("Please enter your name")
            elif not validate_email(signup_email):
                st.error("Please enter a valid email")
            elif not validate_password(signup_password):
                st.error("Password must be at least 6 characters")
            elif signup_password != confirm_password:
                st.error("Passwords do not match!")
            elif signup_email in st.session_state.users:
                st.error("Email already registered!")
            else:
                # Save new user
                st.session_state.users[signup_email] = {
                    'name': signup_name,
                    'email': signup_email,
                    'password': signup_password,  # In real app, hash this!
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_users()
                st.session_state.authenticated = True
                st.session_state.current_user = st.session_state.users[signup_email]
                st.session_state.current_page = 'home'
                st.success(f"Account created successfully! Welcome {signup_name}!")
                st.rerun()
    
    # Back to home button
    if st.button("← Back to Home", key="back_from_auth"):
        st.session_state.current_page = 'home'
        st.rerun()

# ==================== ADDED: JOURNALS INTEGRATION ====================
def show_journals_tab(user_email):
    """Display the journals interface"""
    try:
        from modules.journal import show_journals_page
        show_journals_page(user_email)
    except ImportError as e:
        st.error(f"Journals module not available: {e}")
        st.info("Please install the required dependencies: pip install reportlab Pillow")

def show_account_page():
    """Show user account page with Journals tab"""
    if not st.session_state.authenticated:
        st.error("Please login first!")
        st.session_state.current_page = 'html_auth'
        st.rerun()
        return
    
    user = st.session_state.current_user
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">My Account</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">Welcome back, {user['name']}!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Account statistics
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        trips_count = len(get_user_saved_trips())
        st.metric("Saved Trips", trips_count)
    with col_stats2:
        try:
            from modules.database import get_database
            db = get_database()
            journals_count = len(db.get_user_journals(user['email']))
            st.metric("Travel Journals", journals_count)
        except:
            st.metric("Travel Journals", 0)
    with col_stats3:
        st.metric("Member Since", user.get('created_at', 'Recently').split()[0])
    
    # Navigation tabs
    tabs = ["👤 Profile", "💼 Saved Trips", "📚 My Journals"]
    
    # Create tabs using buttons
    col1, col2, col3 = st.columns(3)
    tab_cols = [col1, col2, col3]
    
    for idx, tab_name in enumerate(tabs):
        with tab_cols[idx]:
            is_active = st.session_state.account_tab == tab_name.lower().replace(" ", "_")
            button_type = "primary" if is_active else "secondary"
            
            if st.button(tab_name, key=f"account_tab_{idx}", type=button_type, use_container_width=True):
                st.session_state.account_tab = tab_name.lower().replace(" ", "_")
                st.rerun()
    
    st.markdown("---")
    
    # Display content based on selected tab
    if st.session_state.account_tab == "profile":
        _show_profile_tab(user)
    elif st.session_state.account_tab == "saved_trips":
        show_saved_trips_section()
    elif st.session_state.account_tab == "my_journals":
        show_journals_tab(user['email'])
    
    # Logout button
    st.markdown("---")
    if st.button("Logout", type="primary", key="account_logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Back button
    if st.button("← Back to Home", key="back_from_account"):
        st.session_state.current_page = 'home'
        st.rerun()

def _show_profile_tab(user):
    """Display profile editing options"""
    st.header("📋 Profile Settings")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name", 
                                    value=user.get('name', ''),
                                    placeholder="Enter your full name")
            
            # Preferences
            st.subheader("Preferences")
            theme = st.selectbox("Theme", 
                                ["Light", "Dark", "Auto"],
                                index=["Light", "Dark", "Auto"].index(
                                    user.get('preferences', {}).get('theme', 'Light')
                                ) if user.get('preferences', {}).get('theme', 'Light') in ["Light", "Dark", "Auto"] else 0)
            
            budget_range = st.selectbox("Budget Range",
                                       ["Budget", "Moderate", "Luxury", "Not set"],
                                       index=["Budget", "Moderate", "Luxury", "Not set"].index(
                                           user.get('preferences', {}).get('budget_range', 'Not set')
                                       ) if user.get('preferences', {}).get('budget_range', 'Not set') in ["Budget", "Moderate", "Luxury", "Not set"] else 3)
        
        with col2:
            # Password change
            st.subheader("Security")
            current_password = st.text_input("Current Password", 
                                            type="password",
                                            placeholder="Enter current password")
            new_password = st.text_input("New Password", 
                                        type="password",
                                        placeholder="Enter new password")
            confirm_password = st.text_input("Confirm New Password", 
                                            type="password",
                                            placeholder="Confirm new password")
            
            # Travel preferences
            st.subheader("Travel Style")
            travel_style = st.multiselect(
                "I prefer",
                ["Adventure", "Relaxation", "Cultural", "Foodie", "Shopping", "Family", "Solo"],
                default=user.get('preferences', {}).get('travel_style', [])
            )
        
        # Submit button
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            submit = st.form_submit_button("💾 Save Changes", type="primary")
        with col_btn2:
            if st.form_submit_button("❌ Cancel"):
                pass
        
        if submit:
            updates = {}
            
            # Update name if changed
            if new_name and new_name != user.get('name'):
                updates['name'] = new_name
            
            # Update preferences
            preferences = user.get('preferences', {}).copy()
            preferences.update({
                'theme': theme,
                'budget_range': budget_range,
                'travel_style': travel_style
            })
            updates['preferences'] = preferences
            
            # Update password if provided
            password_changed = False
            if current_password and new_password and confirm_password:
                if new_password == confirm_password:
                    # Verify current password
                    if user.get('password') == current_password:
                        updates['password'] = new_password
                        password_changed = True
                        st.success("✅ Password updated successfully!")
                    else:
                        st.error("Current password is incorrect")
                else:
                    st.error("New passwords don't match")
            
            # Apply other updates
            if updates:
                st.session_state.users[user['email']].update(updates)
                st.session_state.current_user.update(updates)
                save_users()
                st.success("✅ Profile updated successfully!")
                st.rerun()
            
            if not updates and not password_changed:
                st.info("No changes made to your profile.")

# Import AI Planner
try:
    from modules.ai_planner import render_ai_planner
    AI_PLANNER_AVAILABLE = True
except ImportError as e:
    AI_PLANNER_AVAILABLE = False
    st.warning(f"AI Planner module not available: {e}")

# ==================== CRITICAL FIX: MAKE ALL TEXT BLACK ====================
st.markdown("""
<style>
/* NUCLEAR FIX: MAKE EVERYTHING BLACK ON WHITE */
* {
    color: #000000 !important;
}

/* Force ALL backgrounds WHITE */
body, .stApp, main, [data-testid="stAppViewContainer"] {
    background-color: white !important;
}

/* Force ALL Streamlit text BLACK */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: #000000 !important;
}

/* Force input fields to have BLACK text */
.stTextInput input, .stTextArea textarea, .stSelectbox select,
.stDateInput input, .stNumberInput input, .stMultiSelect input {
    color: #000000 !important;
    background-color: white !important;
    border: 1px solid #cccccc !important;
}

/* Make labels DARK BLUE and BOLD */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stDateInput label, .stCheckbox label,
.stRadio label, .stNumberInput label, .stMultiSelect label {
    color: #1a237e !important;
    font-weight: bold !important;
    font-size: 16px !important;
}

/* Make containers white with borders */
.stContainer, .element-container, .block-container {
    background-color: white !important;
}

/* Custom styling for expander headers (Day1, Day2 buttons) */
.stExpander {
    border: 2px solid #1e88e5 !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
}

/* Make Day1, Day2 buttons LIGHT BLUE */
.stExpander > summary {
    background-color: #e3f2fd !important;
    color: #000000 !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    padding: 12px 20px !important;
    border-radius: 8px !important;
}

/* Hover effect for expander headers */
.stExpander > summary:hover {
    background-color: #bbdefb !important;
}

/* Content inside expanders - ensure black text */
.stExpander .streamlit-expanderContent {
    color: #000000 !important;
    padding: 15px !important;
}

/* Force ALL markdown text to be black */
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #000000 !important;
}

/* Navigation styling */
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 50px;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    border-bottom: 1px solid #eee;
    background: #fff;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.logo {
    font-size: 24px;
    font-weight: 700;
    color: #2E65F3;
    letter-spacing: 1px;
    cursor: pointer;
}
.links {
    display: flex;
    gap: 25px;
    font-size: 15px;
    font-weight: 500;
    margin-left: auto;
    margin-right: 30px;
}
.links a {
    color: #222;
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 4px;
    transition: all 0.2s;
}
.links a:hover {
    color: #2E65F3;
    background-color: #f0f0f0;
}
.auth-container {
    display: flex;
    gap: 12px;
    align-items: center;
}
.auth-btn {
    border: 1px solid #2E65F3;
    background: transparent;
    font-size: 14px;
    font-weight: 600;
    color: #2E65F3;
    cursor: pointer;
    padding: 8px 20px;
    border-radius: 6px;
    transition: all 0.2s;
}
.auth-btn:hover {
    background-color: #2E65F3;
    color: white;
}
.auth-btn-primary {
    background: #2E65F3;
    color: white;
    border: 1px solid #2E65F3;
}
.auth-btn-primary:hover {
    background: #1e4fcf;
    border-color: #1e4fcf;
}
.hero {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    padding: 80px 50px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    min-height: 80vh;
}
.hero-content {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    max-width: 1200px;
    width: 100%;
    gap: 40px;
}
.hero-text {
    flex: 1;
    min-width: 300px;
    text-align: center;
}
.hero-text h1 {
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 20px;
    color: white !important; /* Keep hero text white */
}
.hero-text p {
    font-size: 1.2rem;
    line-height: 1.6;
    margin-bottom: 30px;
    opacity: 0.9;
    color: white !important; /* Keep hero text white */
}
.hero-buttons {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
}
.btn-primary {
    background-color: #FF6B6B;
    color: white !important;
    border: none;
    padding: 15px 30px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}
.btn-primary:hover {
    background-color: #ff5252;
    transform: translateY(-2px);
}
.btn-secondary {
    background-color: transparent;
    color: white !important;
    border: 2px solid white;
    padding: 15px 30px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}
.btn-secondary:hover {
    background-color: white;
    color: #667eea !important;
}
.features {
    padding: 80px 50px;
    background-color: #f8f9fa;
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 40px;
    max-width: 1200px;
    margin: 0 auto;
}
.feature-card {
    background: white;
    padding: 40px 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}
.feature-card:hover {
    transform: translateY(-5px);
}
.feature-icon {
    font-size: 3rem;
    margin-bottom: 20px;
}
.feature-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #000000 !important;
    margin-bottom: 15px;
}
.feature-desc {
    color: #666 !important;
    line-height: 1.6;
}
.why-choose {
    padding: 80px 50px;
    background: white;
}
.why-choose-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 40px;
    max-width: 1200px;
    margin: 0 auto;
}
.why-choose-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    padding: 40px 30px;
    border-radius: 15px;
    border-left: 5px solid #2E65F3;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}
.why-choose-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}
.why-choose-number {
    font-size: 3rem;
    font-weight: 900;
    color: #2E65F3 !important;
    margin-bottom: 15px;
    opacity: 0.8;
}
.why-choose-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #000000 !important;
    margin-bottom: 15px;
}
.why-choose-desc {
    color: #555 !important;
    line-height: 1.7;
    font-size: 1.05rem;
}
@media(max-width: 768px){
    .nav { padding: 15px 20px; }
    .hero { padding: 40px 20px; }
    .hero-text h1 { font-size: 2.5rem; }
    .features, .why-choose { padding: 40px 20px; }
    .links { margin-right: 15px; }
}
</style>
""", unsafe_allow_html=True)

# Hide default Streamlit elements
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
       header {visibility: hidden;}
       .stDeployButton {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# ============================================================================
# DESTINATION ITINERARY PAGES (WITH BLACK TEXT AND SAVE TRIP FUNCTIONALITY)
# ============================================================================

def create_dubai_plan_page():
    """Create the Dubai trip plan page"""
    # Back button
    if st.button("← Back to Home", key="back_from_dubai"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Save trip button - FIXED POSITION
    if st.session_state.authenticated:
        # Create a container for the save button at the top
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col3:
                if st.button("💾 Save This Trip", key="save_dubai", type="primary", use_container_width=True):
                    # Show save dialog
                    with st.popover("💾 Save Trip", use_container_width=True):
                        trip_name = st.text_input("Trip Name", value="Dubai Luxury Adventure - 7 Days")
                        if st.button("Save Trip", key="confirm_save_dubai", type="primary"):
                            if trip_name.strip():
                                # Prepare itinerary data for saving
                                itinerary_data = {
                                    'highlights': [
                                        "Burj Khalifa - World's tallest building",
                                        "Dubai Mall - Largest shopping mall",
                                        "Desert Safari with dune bashing",
                                        "Old Dubai souk exploration",
                                        "Abu Dhabi day trip",
                                        "Dhow dinner cruise"
                                    ],
                                    'day_plans': [
                                        {
                                            'day': 'DAY 1',
                                            'title': 'Arrival + Downtown Dubai',
                                            'activities': [
                                                'Land at DXB Airport',
                                                'Check-in at hotel',
                                                'Visit Dubai Mall',
                                                'Burj Khalifa Observation Deck',
                                                'Dubai Fountain Show'
                                            ]
                                        },
                                        {
                                            'day': 'DAY 2',
                                            'title': 'Old Dubai Heritage',
                                            'activities': [
                                                'Al Fahidi Historical District',
                                                'Dubai Museum',
                                                'Abra boat ride',
                                                'Gold & Spice Souks',
                                                'Dhow dinner cruise'
                                            ]
                                        }
                                    ],
                                    'budget_breakdown': {
                                        'Flight (India to Dubai)': '₹18,000 – ₹35,000',
                                        'Hotel (3★, 7 nights)': '₹18,000 – ₹28,000',
                                        'Food & Dining': '₹8,000 – ₹14,000',
                                        'Local Transport': '₹3,000 – ₹6,000',
                                        'Activities & Tours': '₹14,000 – ₹22,000',
                                        'Shopping (optional)': '₹3,000 – ₹50,000+'
                                    }
                                }
                                
                                if save_current_trip(
                                    trip_name=trip_name,
                                    destination="Dubai",
                                    duration="7 days",
                                    budget="₹60,000 – ₹1,25,000 per person",
                                    itinerary_data=itinerary_data
                                ):
                                    st.rerun()
                            else:
                                st.error("Please enter a trip name!")
    
    # Header (BLACK TEXT)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">Dubai Trip Plan</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">7-Day Luxury & Adventure Experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Highlights (BLACK TEXT)
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>✨ Trip Highlights</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🏙️ Iconic Landmarks:**
            - Burj Khalifa - World's tallest building
            - Dubai Mall - Largest shopping mall
            - Dubai Fountain - Spectacular water show
            - Palm Jumeirah - Iconic man-made island
            """)
        with col2:
            st.markdown("""
            **🏜️ Unique Experiences:**
            - Desert Safari with dune bashing
            - Old Dubai souk exploration
            - Abu Dhabi day trip
            - Dhow dinner cruise
            """)
    
    # 7-Day Itinerary (BLACK TEXT with LIGHT BLUE DAY BUTTONS)
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🗓️ 7-Day Detailed Itinerary</h2>", unsafe_allow_html=True)
        
        days = [
            ("DAY 1", "Arrival + Downtown Dubai", 
             ["Land at DXB Airport", "Check-in at hotel", "Visit Dubai Mall", "Burj Khalifa Observation Deck", "Dubai Fountain Show"]),
            
            ("DAY 2", "Old Dubai Heritage",
             ["Al Fahidi Historical District", "Dubai Museum", "Abra boat ride", "Gold & Spice Souks", "Dhow dinner cruise"]),
            
            ("DAY 3", "Desert Safari Adventure",
             ["Morning free time", "3:00 PM safari pickup", "Dune bashing", "Camel ride", "Sunset photos", "BBQ dinner with shows"]),
            
            ("DAY 4", "Beach + Palm Jumeirah",
             ["Jumeirah Beach", "Burj Al Arab photo stop", "Palm Jumeirah monorail", "Atlantis The Palm", "Dubai Marina walk"]),
            
            ("DAY 5", "Abu Dhabi Day Trip",
             ["Sheikh Zayed Grand Mosque", "Heritage Village", "Louvre Abu Dhabi (optional)", "Return to Dubai"]),
            
            ("DAY 6", "Miracle Garden + Global Village",
             ["Dubai Miracle Garden", "Butterfly dome", "Global Village exploration", "Cultural shows", "Shopping"]),
            
            ("DAY 7", "Departure",
             ["Last-minute shopping", "Dubai Duty Free", "Transfer to airport", "Departure"])
        ]
        
        for day_num, day_title, activities in days:
            with st.expander(f"{day_num}: {day_title}", expanded=(day_num=="DAY 1")):
                for activity in activities:
                    st.markdown(f"• {activity}")
    
    # Budget (BLACK TEXT)
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>💰 Estimated Budget (Per Person)</h2>", unsafe_allow_html=True)

        # CSS to right-align cost values
        st.markdown("""<style>.right-align {text-align: right !important;display: block;}</style>""", unsafe_allow_html=True)

        budget_data = {
            "Flight (India to Dubai)": "₹18,000 – ₹35,000",
            "Hotel (3★, 7 nights)": "₹18,000 – ₹28,000",
            "Food & Dining": "₹8,000 – ₹14,000",
            "Local Transport": "₹3,000 – ₹6,000",
            "Activities & Tours": "₹14,000 – ₹22,000",
            "Shopping (optional)": "₹3,000 – ₹50,000+"
        }

        for item, cost in budget_data.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                st.markdown(f"<span class='right-align'>{cost}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**✅ Total Estimated: ₹60,000 – ₹1,25,000 per person**")

    
    # Packing Checklist (BLACK TEXT)
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🎒 Packing Checklist</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Essential Items:**
            - Light breathable clothes
            - Sunscreen & sunglasses
            - Comfortable walking shoes
            - Swimwear
            """)
        with col2:
            st.markdown("""
            **Important Documents:**
            - Passport with visa
            - Hotel confirmations
            - Travel insurance
            - Power bank & adapter
            """)

def create_thailand_plan_page():
    """Create the Thailand trip plan page"""
    # Back button
    if st.button("← Back to Home", key="back_from_thailand"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Save trip button
    if st.session_state.authenticated:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col3:
                if st.button("💾 Save This Trip", key="save_thailand", type="primary", use_container_width=True):
                    # Show save dialog
                    with st.popover("💾 Save Trip", use_container_width=True):
                        trip_name = st.text_input("Trip Name", value="Thailand Adventure - 10 Days")
                        if st.button("Save Trip", key="confirm_save_thailand", type="primary"):
                            if trip_name.strip():
                                if save_current_trip(
                                    trip_name=trip_name,
                                    destination="Thailand",
                                    duration="10 days",
                                    budget="₹70,000 – ₹1,21,000 per person"
                                ):
                                    st.rerun()
                            else:
                                st.error("Please enter a trip name!")
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">Thailand Trip Plan</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">10-Day Cultural & Island Adventure</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Highlights
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>✨ Trip Highlights</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🏛️ Cultural Wonders:**
            - Grand Palace Bangkok
            - Wat Arun & Wat Pho
            - Chiang Mai temples
            - Floating markets
            """)
        with col2:
            st.markdown("""
            **🏝️ Island Paradise:**
            - Phi Phi Islands day trip
            - Phuket beaches
            - Thai cooking class
            - Elephant sanctuary
            """)
    
    # 10-Day Itinerary
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🗓️ 10-Day Detailed Itinerary</h2>", unsafe_allow_html=True)
        
        days = [
            ("DAY 1", "Arrival in Bangkok", 
             ["Land at BKK Airport", "Check-in at hotel", "Wat Arun visit", "Chao Phraya River cruise", "Asiatique Night Market"]),
            
            ("DAY 2", "Bangkok Temples & Markets",
             ["Grand Palace & Emerald Buddha", "Wat Pho (Reclining Buddha)", "Jim Thompson House", "Chinatown street food"]),
            
            ("DAY 3", "Floating Markets + Cooking",
             ["Damnoen Saduak Floating Market", "Thai cooking class", "Learn Tom Yum & Pad Thai", "Rot Fai Train Market"]),
            
            ("DAY 4", "Fly to Chiang Mai",
             ["Flight to Chiang Mai", "Doi Suthep temple", "Bhuping Palace", "Chiang Mai Night Bazaar"]),
            
            ("DAY 5", "Elephant Sanctuary",
             ["Ethical elephant sanctuary", "Feed & bathe elephants", "Thai cooking class", "Nimmanhaemin Road cafes"]),
            
            ("DAY 6", "Fly to Phuket",
             ["Chiang Mai temples", "Flight to Phuket", "Patong Beach relaxation", "Bangla Road nightlife"]),
        ]
        
        for day_num, day_title, activities in days:
            with st.expander(f"{day_num}: {day_title}", expanded=(day_num=="DAY 1")):
                for activity in activities:
                    st.markdown(f"• {activity}")
        
        st.info("**Days 7-10:** Phi Phi Islands, James Bond Island, beach relaxation, and departure")
    
    # Budget
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>💰 Estimated Budget (Per Person)</h2>", unsafe_allow_html=True)

        # Right align cost values
        st.markdown("""<style>.right-align {text-align: right !important;display: block;}</style>""", unsafe_allow_html=True)

        budget_data = {
            "Flight (India to Bangkok)": "₹15,000 – ₹25,000",
            "Domestic Flights": "₹8,000 – ₹12,000",
            "Hotel (3★, 7 nights)": "₹20,000 – ₹30,000",
            "Food & Dining": "₹6,000 – ₹10,000",
            "Transport & Tours": "₹16,000 – ₹24,000",
            "Shopping (optional)": "₹5,000 – ₹20,000+"
        }

        for item, cost in budget_data.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                st.markdown(f"<span class='right-align'>{cost}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**✅ Total Estimated: ₹70,000 – ₹1,21,000 per person**")

    
    # Packing Checklist
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🎒 Packing Checklist</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **For Thailand:**
            - Light cotton clothes
            - Swimwear & beach essentials
            - Comfortable walking shoes
            - Rain jacket/umbrella
            """)
        with col2:
            st.markdown("""
            **Important Items:**
            - Passport with visa
            - Modest temple clothing
            - Mosquito repellent
            - Universal adapter
            """)

def create_georgia_plan_page():
    """Create the Georgia trip plan page"""
    # Back button
    if st.button("← Back to Home", key="back_from_georgia"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Save trip button
    if st.session_state.authenticated:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col3:
                if st.button("💾 Save This Trip", key="save_georgia", type="primary", use_container_width=True):
                    # Show save dialog
                    with st.popover("💾 Save Trip", use_container_width=True):
                        trip_name = st.text_input("Trip Name", value="Georgia Mountain Adventure - 6 Days")
                        if st.button("Save Trip", key="confirm_save_georgia", type="primary"):
                            if trip_name.strip():
                                if save_current_trip(
                                    trip_name=trip_name,
                                    destination="Georgia",
                                    duration="6 days",
                                    budget="₹68,000 – ₹1,10,000 per person"
                                ):
                                    st.rerun()
                            else:
                                st.error("Please enter a trip name!")
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">Georgia Trip Plan</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">6-Day Cultural & Mountain Adventure</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Highlights
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>✨ Trip Highlights</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🏰 Cultural Gems:**
            - Old Tbilisi walking tour
            - Narikala Fortress
            - Georgian wine tasting
            - Sulfur baths experience
            """)
        with col2:
            st.markdown("""
            **⛰️ Mountain Wonders:**
            - Kazbegi mountain views
            - Gergeti Trinity Church
            - Georgian Military Highway
            - Ananuri Fortress
            """)
    
    # 6-Day Itinerary
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🗓️ 6-Day Detailed Itinerary</h2>", unsafe_allow_html=True)
        
        days = [
            ("DAY 1", "Arrival in Tbilisi", 
             ["Tbilisi International Airport", "Hotel check-in", "Old Tbilisi exploration", "Sulfur Bath District", "Traditional Georgian dinner"]),
            
            ("DAY 2", "Tbilisi City Tour",
             ["Holy Trinity Cathedral", "Dry Bridge Market", "Rustaveli Avenue", "Georgian wine tasting", "Traditional Supra feast"]),
            
            ("DAY 3", "Mtskheta + Kazbegi",
             ["Ancient capital Mtskheta", "Svetitskhoveli Cathedral", "Jvari Monastery", "Georgian Military Highway", "Arrive in Kazbegi"]),
            
            ("DAY 4", "Kazbegi Mountain Day",
             ["4x4 to Gergeti Trinity Church", "Mountain hiking", "Gveleti Waterfalls", "Dariali Gorge", "Return to Tbilisi"]),
            
            ("DAY 5", "Kakheti Wine Region",
             ["Drive to Kakheti", "Bodbe Monastery", "Sighnaghi 'City of Love'", "Wine tasting at vineyard", "Traditional lunch"]),
            
            ("DAY 6", "Departure",
             ["Breakfast at hotel", "Last souvenir shopping", "Fabrika creative space", "Transfer to airport", "Departure"])
        ]
        
        for day_num, day_title, activities in days:
            with st.expander(f"{day_num}: {day_title}", expanded=(day_num=="DAY 1")):
                for activity in activities:
                    st.markdown(f"• {activity}")
    
    # Budget
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>💰 Estimated Budget (Per Person)</h2>", unsafe_allow_html=True)

        # Right-align cost values
        st.markdown("""<style>.right-align {text-align: right !important;display: block;}</style>""", unsafe_allow_html=True)

        budget_data = {
            "Flight (India to Tbilisi)": "₹25,000 – ₹40,000",
            "Accommodation (5 nights)": "₹15,000 – ₹25,000",
            "Food & Dining": "₹8,000 – ₹12,000",
            "Transport & Tours": "₹10,000 – ₹15,000",
            "Wine Tasting & Activities": "₹5,000 – ₹8,000",
            "Shopping": "₹5,000 – ₹10,000"
        }

        for item, cost in budget_data.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                st.markdown(f"<span class='right-align'>{cost}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**✅ Total Estimated: ₹68,000 – ₹1,10,000 per person**")

    
    # Packing Checklist
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🎒 Packing Checklist</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Clothing:**
            - Layered clothing
            - Warm jacket for mountains
            - Comfortable hiking shoes
            - Rainproof jacket
            """)
        with col2:
            st.markdown("""
            **Essentials:**
            - Passport (visa-free for Indians)
            - European Type C/F adapter
            - Camera for scenic photos
            - Basic medicines
            """)

def create_maldives_plan_page():
    """Create the Maldives trip plan page"""
    # Back button
    if st.button("← Back to Home", key="back_from_maldives"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Save trip button
    if st.session_state.authenticated:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col3:
                if st.button("💾 Save This Trip", key="save_maldives", type="primary", use_container_width=True):
                    # Show save dialog
                    with st.popover("💾 Save Trip", use_container_width=True):
                        trip_name = st.text_input("Trip Name", value="Maldives Luxury Getaway - 5 Days")
                        if st.button("Save Trip", key="confirm_save_maldives", type="primary"):
                            if trip_name.strip():
                                if save_current_trip(
                                    trip_name=trip_name,
                                    destination="Maldives",
                                    duration="5 days",
                                    budget="₹98,000 – ₹1,90,000 per person"
                                ):
                                    st.rerun()
                            else:
                                st.error("Please enter a trip name!")
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">Maldives Trip Plan</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">5-Day Luxury Island Paradise</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Highlights
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>✨ Trip Highlights</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🏝️ Island Paradise:**
            - Overwater bungalow stay
            - Crystal clear turquoise waters
            - Private beach access
            - Stunning sunsets
            """)
        with col2:
            st.markdown("""
            **🤿 Water Adventures:**
            - Snorkeling with marine life
            - Scuba diving (PADI certified)
            - Dolphin watching cruise
            - Sunset fishing
            """)
    
    # 5-Day Itinerary
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🗓️ 5-Day Detailed Itinerary</h2>", unsafe_allow_html=True)
        
        days = [
            ("DAY 1", "Arrival + Resort Check-in", 
             ["Arrive at Male Airport", "Speedboat to resort", "Overwater villa check-in", "Beach relaxation", "Welcome dinner"]),
            
            ("DAY 2", "Island Exploration",
             ["Breakfast with ocean view", "Snorkeling session", "Resort facilities tour", "Spa treatment", "Sunset cruise"]),
            
            ("DAY 3", "Water Sports Day",
             ["Scuba diving (optional)", "Jet skiing", "Kayaking", "Stand-up paddleboarding", "Beach BBQ dinner"]),
            
            ("DAY 4", "Excursion Day",
             ["Dolphin watching tour", "Visit local island", "Cultural experience", "Shopping for souvenirs", "Farewell dinner"]),
            
            ("DAY 5", "Departure",
             ["Last swim in ocean", "Breakfast at villa", "Check-out", "Speedboat to airport", "Departure"])
        ]
        
        for day_num, day_title, activities in days:
            with st.expander(f"{day_num}: {day_title}", expanded=(day_num=="DAY 1")):
                for activity in activities:
                    st.markdown(f"• {activity}")
    
    # Budget
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>💰 Estimated Budget (Per Person)</h2>", unsafe_allow_html=True)

        # Right-align cost values
        st.markdown("""<style>.right-align {text-align: right !important;display: block;}</style>""", unsafe_allow_html=True)

        budget_data = {
            "Flight (India to Male)": "₹20,000 – ₹35,000",
            "Resort (4★, 4 nights)": "₹40,000 – ₹80,000",
            "Speedboat Transfer": "₹8,000 – ₹15,000",
            "Food & Dining": "₹15,000 – ₹25,000",
            "Activities & Spa": "₹10,000 – ₹20,000",
            "Shopping": "₹5,000 – ₹15,000"
        }

        for item, cost in budget_data.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                st.markdown(f"<span class='right-align'>{cost}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**✅ Total Estimated: ₹98,000 – ₹1,90,000 per person**")
        st.info("*Price varies greatly based on resort selection and season*")

    
    # Packing Checklist
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🎒 Packing Checklist</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Beach Essentials:**
            - Swimwear (multiple)
            - Beach cover-ups
            - Sun hat & sunglasses
            - Reef-safe sunscreen
            """)
        with col2:
            st.markdown("""
            **Important Items:**
            - Passport (30-day visa on arrival)
            - Underwater camera
            - Beach bag
            - Flip flops/sandals
            """)

def create_paris_plan_page():
    """Create the Paris trip plan page"""
    # Back button
    if st.button("← Back to Home", key="back_from_paris"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Save trip button
    if st.session_state.authenticated:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col3:
                if st.button("💾 Save This Trip", key="save_paris", type="primary", use_container_width=True):
                    # Show save dialog
                    with st.popover("💾 Save Trip", use_container_width=True):
                        trip_name = st.text_input("Trip Name", value="Paris Romantic Getaway - 6 Days")
                        if st.button("Save Trip", key="confirm_save_paris", type="primary"):
                            if trip_name.strip():
                                if save_current_trip(
                                    trip_name=trip_name,
                                    destination="Paris",
                                    duration="6 days",
                                    budget="₹1,10,000 – ₹1,88,000 per person"
                                ):
                                    st.rerun()
                            else:
                                st.error("Please enter a trip name!")
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">Paris Trip Plan</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">6-Day Romantic European Getaway</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Highlights
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>✨ Trip Highlights</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🗼 Iconic Landmarks:**
            - Eiffel Tower visit
            - Louvre Museum
            - Notre-Dame Cathedral
            - Arc de Triomphe
            """)
        with col2:
            st.markdown("""
            **🍷 Parisian Experiences:**
            - Seine River cruise
            - Montmartre exploration
            - French cuisine tasting
            - Champs-Élysées shopping
            """)
    
    # 6-Day Itinerary
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🗓️ 6-Day Detailed Itinerary</h2>", unsafe_allow_html=True)
        
        days = [
            ("DAY 1", "Arrival + Eiffel Tower", 
             ["Arrive at CDG Airport", "Hotel check-in", "Eiffel Tower visit", "Trocadéro Gardens", "River Seine walk"]),
            
            ("DAY 2", "Louvre + Notre-Dame",
             ["Louvre Museum (Mona Lisa)", "Tuileries Garden", "Notre-Dame Cathedral", "Latin Quarter", "French dinner"]),
            
            ("DAY 3", "Montmartre + Sacré-Cœur",
             ["Sacré-Cœur Basilica", "Montmartre artists' square", "Moulin Rouge photo", "Place du Tertre", "Bohemian Paris tour"]),
            
            ("DAY 4", "Versailles Day Trip",
             ["Train to Versailles", "Palace of Versailles", "Hall of Mirrors", "Gardens of Versailles", "Return to Paris"]),
            
            ("DAY 5", "Shopping & Museums",
             ["Champs-Élysées", "Arc de Triomphe", "Musée d'Orsay", "Luxembourg Gardens", "Evening Seine cruise"]),
            
            ("DAY 6", "Departure",
             ["Last croissant breakfast", "Souvenir shopping", "Visit local patisserie", "Transfer to airport", "Au revoir Paris!"])
        ]
        
        for day_num, day_title, activities in days:
            with st.expander(f"{day_num}: {day_title}", expanded=(day_num=="DAY 1")):
                for activity in activities:
                    st.markdown(f"• {activity}")
    
    # Budget
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>💰 Estimated Budget (Per Person)</h2>", unsafe_allow_html=True)

        # Right-align cost values
        st.markdown("""<style>.right-align {text-align: right !important;display: block;}</style>""", unsafe_allow_html=True)

        budget_data = {
            "Flight (India to Paris)": "₹40,000 – ₹70,000",
            "Hotel (3★, 5 nights)": "₹35,000 – ₹55,000",
            "Food & Dining": "₹20,000 – ₹30,000",
            "Transport & Tours": "₹10,000 – ₹18,000",
            "Museums & Attractions": "₹5,000 – ₹10,000",
            "Shopping": "₹5,000 – ₹15,000"
        }

        for item, cost in budget_data.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                st.markdown(f"<span class='right-align'>{cost}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**✅ Total Estimated: ₹1,15,000 – ₹1,98,000 per person**")

    
    # Packing Checklist
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🎒 Packing Checklist</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Parisian Style:**
            - Smart casual outfits
            - Comfortable walking shoes
            - Light jacket (all seasons)
            - Umbrella (just in case)
            """)
        with col2:
            st.markdown("""
            **Essentials:**
            - Passport with Schengen visa
            - European Type E adapter
            - Museum pass (pre-booked)
            - French phrasebook app
            """)

def create_bali_plan_page():
    """Create the Bali trip plan page"""
    # Back button
    if st.button("← Back to Home", key="back_from_bali"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    # Save trip button
    if st.session_state.authenticated:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col3:
                if st.button("💾 Save This Trip", key="save_bali", type="primary", use_container_width=True):
                    # Show save dialog
                    with st.popover("💾 Save Trip", use_container_width=True):
                        trip_name = st.text_input("Trip Name", value="Bali Tropical Escape - 8 Days")
                        if st.button("Save Trip", key="confirm_save_bali", type="primary"):
                            if trip_name.strip():
                                if save_current_trip(
                                    trip_name=trip_name,
                                    destination="Bali",
                                    duration="8 days",
                                    budget="₹78,000 – ₹1,30,000 per person"
                                ):
                                    st.rerun()
                            else:
                                st.error("Please enter a trip name!")
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">Bali Trip Plan</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">8-Day Tropical Island Paradise</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Trip Highlights
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>✨ Trip Highlights</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🕌 Cultural Bali:**
            - Ubud art & culture
            - Tanah Lot Temple
            - Uluwatu Temple
            - Traditional dance shows
            """)
        with col2:
            st.markdown("""
            **🏖️ Natural Beauty:**
            - Rice terrace walks
            - Waterfall visits
            - Beach club relaxation
            - Monkey Forest
            """)
    
    # 8-Day Itinerary
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🗓️ 8-Day Detailed Itinerary</h2>", unsafe_allow_html=True)
        
        days = [
            ("DAY 1", "Arrival + Seminyak", 
             ["Arrive at DPS Airport", "Transfer to Seminyak", "Beach relaxation", "Seminyak Square", "Beach club sunset"]),
            
            ("DAY 2", "Ubud Cultural Day",
             ["Drive to Ubud", "Sacred Monkey Forest", "Ubud Art Market", "Traditional dance show", "Rice terrace view"]),
            
            ("DAY 3", "Ubud Exploration",
             ["Tegalalang Rice Terrace", "Coffee plantation tour", "Tirta Empul Temple", "Ubud Palace", "Cooking class"]),
            
            ("DAY 4", "Waterfalls + North Bali",
             ["Gitgit Waterfall", "Ulun Danu Temple", "Jatiluwih Rice Terraces", "Return to Ubud", "Spa treatment"]),
            
            ("DAY 5", "South Bali Beaches",
             ["Transfer to Uluwatu", "Padang Padang Beach", "Uluwatu Temple", "Kecak fire dance", "Jimbaran seafood dinner"]),
            
            ("DAY 6", "Nusa Penida Day Trip",
             ["Speedboat to Nusa Penida", "Kelingking Beach", "Angel's Billabong", "Broken Beach", "Return to Bali"])
        ]
        
        for day_num, day_title, activities in days:
            with st.expander(f"{day_num}: {day_title}", expanded=(day_num=="DAY 1")):
                for activity in activities:
                    st.markdown(f"• {activity}")
        
        st.info("**Days 7-8:** Free day for shopping, spa, beach time, and departure")
    
    # Budget
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>💰 Estimated Budget (Per Person)</h2>", unsafe_allow_html=True)

        # Right-align cost values
        st.markdown("""<style>.right-align {text-align: right !important;display: block;}</style>""", unsafe_allow_html=True)

        budget_data = {
            "Flight (India to Bali)": "₹18,000 – ₹30,000",
            "Hotel/Villa (7 nights)": "₹25,000 – ₹40,000",
            "Food & Dining": "₹12,000 – ₹18,000",
            "Transport & Tours": "₹10,000 – ₹15,000",
            "Activities & Spa": "₹8,000 – ₹12,000",
            "Shopping": "₹5,000 – ₹15,000"
        }

        for item, cost in budget_data.items():
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                st.markdown(f"<span class='right-align'>{cost}</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**✅ Total Estimated: ₹78,000 – ₹1,30,000 per person**")

    
    # Packing Checklist
    with st.container(border=True):
        st.markdown("<h2 style='color: black !important;'>🎒 Packing Checklist</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Tropical Clothing:**
            - Light summer clothes
            - Swimwear & cover-ups
            - Temple-appropriate attire
            - Comfortable sandals
            """)
        with col2:
            st.markdown("""
            **Bali Essentials:**
            - Passport (visa-free for Indians)
            - Mosquito repellent
            - Reef-safe sunscreen
            - Universal adapter
            """)

def create_destinations_page():
    """Create a destinations showcase page"""
    # FIXED: Removed duplicate heading
    
    
    # Create destination grid
    destinations = [
        {
            "name": "Dubai",
            "description": "7-Day Luxury & Adventure",
            "budget": "₹60K - ₹1.25L",
            "duration": "7 days",
            "image": "🏙️",
            "page": "dubai_plan"
        },
        {
            "name": "Thailand",
            "description": "10-Day Cultural & Islands",
            "budget": "₹70K - ₹1.21L",
            "duration": "10 days",
            "image": "🏝️",
            "page": "thailand_plan"
        },
        {
            "name": "Georgia",
            "description": "6-Day Mountains & Wine",
            "budget": "₹68K - ₹1.1L",
            "duration": "6 days",
            "image": "⛰️",
            "page": "georgia_plan"
        },
        {
            "name": "Maldives",
            "description": "5-Day Luxury Paradise",
            "budget": "₹98K - ₹1.9L",
            "duration": "5 days",
            "image": "🤿",
            "page": "maldives_plan"
        },
        {
            "name": "Paris",
            "description": "6-Day Romantic Europe",
            "budget": "₹1.1L - ₹1.88L",
            "duration": "6 days",
            "image": "🗼",
            "page": "paris_plan"
        },
        {
            "name": "Bali",
            "description": "8-Day Tropical Escape",
            "budget": "₹78K - ₹1.3L",
            "duration": "8 days",
            "image": "🕌",
            "page": "bali_plan"
        }
    ]
    
    # Create 3 columns for the grid
    cols = st.columns(3)
    
    for idx, destination in enumerate(destinations):
        with cols[idx % 3]:
            with st.container(border=True, height=300):
                st.markdown(f"<div style='text-align: center; font-size: 4rem; margin: 20px 0;'>{destination['image']}</div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: black !important;'>{destination['name']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: #666 !important;'>{destination['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: #2E65F3 !important; font-weight: bold;'>Budget: {destination['budget']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: #666 !important;'>Duration: {destination['duration']}</p>", unsafe_allow_html=True)
                
                # Button to view plan
                if st.button(f"View {destination['name']} Plan", key=f"view_{destination['page']}", use_container_width=True):
                    st.session_state.current_page = destination['page']
                    st.rerun()
    
    # Call to action for AI Planner
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white !important;">
            <h3 style="color: white !important; margin-bottom: 15px;">Want a Custom Itinerary?</h3>
            <p style="color: white !important;">Create your own personalized travel plan with our AI Planner!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Try AI Travel Planner", use_container_width=True, type="primary"):
            if AI_PLANNER_AVAILABLE:
                st.session_state.current_page = 'ai_planner'
                st.rerun()
            else:
                st.error("AI Planner not available")

# ============================================================================
# MAIN APPLICATION ROUTING
# ============================================================================

# Navigation bar - UPDATED WITH FLIGHTS AND AVATAR
# Floating Chatbot Popover
render_chatbot_popover()

# Navigation bar
st.markdown("""
<style>
/* Shift Nav padding back to normal or keep slightly adjusted if needed */
.nav {
    padding-left: 80px !important;
}
</style>

<div class="nav">
    <div class="logo" onclick="window.location.href=window.location.origin + '?page=home'">Travelume</div>
    <div class="links">
        <a href="#destinations">Destinations</a>
        <a href="#ai-planner">AI Planner</a>
        <a href="#features">Features</a>
        <a href="#flight-booking">✈️ Flights</a>
        <a href="#hotel-booking">🏨 Hotels</a>
    </div>
    <div class="auth-container">
""", unsafe_allow_html=True)

# Create columns to position buttons in top right
col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    if st.session_state.authenticated:
        if st.button("My Account", key="nav_account", use_container_width=True):
            st.session_state.current_page = 'account'
            st.rerun()
    else:
        if st.button("Sign Up", key="nav_signup", use_container_width=True):
            st.session_state.current_page = 'html_auth'
            st.rerun()
with col3:
    if st.session_state.authenticated:
        if st.button("Logout", key="nav_logout", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.current_page = 'home'
            st.rerun()
    else:
        if st.button("Login", key="nav_login", type="primary", use_container_width=True):
            st.session_state.current_page = 'html_auth'
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Show appropriate page based on current_page
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-text">
                <h1>AI-Powered Travel Planning</h1>
                <p>
                    Create perfect travel itineraries in minutes. Personalized to your style, 
                    budget, and preferences with advanced AI technology.
                </p>
                <div class="hero-buttons">
    """, unsafe_allow_html=True)

    # Main AI Planner button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 Try AI Planner", key="hero_ai", use_container_width=True):
            if AI_PLANNER_AVAILABLE:
                st.session_state.current_page = 'ai_planner'
                st.rerun()
            else:
                st.error("AI Planner not available yet")
    with col2:
        if st.button("🌍 Browse Destinations", key="hero_destinations", use_container_width=True):
            st.session_state.current_page = 'destinations'
            st.rerun()
    
    # Transportation/Hotel buttons - UPDATED
    st.markdown("""
    <div style="margin-top: 30px; text-align: center;">
        <p style="color: white !important; margin-bottom: 15px; font-size: 1.1rem;">
            <strong>Book Travel Essentials:</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create 6 buttons in 2 rows - UPDATED
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✈️ Flights", key="hero_flights", use_container_width=True):
            st.session_state.current_page = 'flight_booking'  # CHANGED THIS LINE
            st.rerun()
    with col2:
        if st.button("🚆 Trains", key="hero_trains", use_container_width=True):
            st.info("Train booking coming soon!")
    with col3:
        if st.button("🚌 Buses", key="hero_buses", use_container_width=True):
            st.info("Bus booking coming soon!")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🏨 Hotels", key="hero_hotels2", use_container_width=True):
            st.session_state.current_page = 'hotel_booking'
            st.rerun()
    with col5:
        if st.button("🏡 Villas", key="hero_villas", use_container_width=True):
            st.info("Villa booking coming soon!")
    with col6:
        if st.button("🚗 Car Rental", key="hero_cars", use_container_width=True):
            st.info("Car rental coming soon!")
    
    st.markdown("""
                </div>
                <p style="margin-top: 20px; font-size: 16px; opacity: 0.8;">
                    Free to use • No credit card required • Instant itineraries
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Destinations Preview - FIXED: Only one heading
    st.markdown("""
    <div id="destinations" style="padding: 80px 50px;">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 2.5rem; color: #333 !important; margin-bottom: 20px;">Popular Destinations</h2>
            <p style="font-size: 1.2rem; color: #666 !important; max-width: 600px; margin: 0 auto;">
                Ready-made itineraries for your next adventure
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    create_destinations_page()

    # Features Section
    st.markdown("""
    <div id="features" class="features">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 2.5rem; color: #333 !important; margin-bottom: 20px;">How It Works</h2>
            <p style="font-size: 1.2rem; color: #666 !important; max-width: 600px; margin: 0 auto;">
                Simple steps to create your perfect travel itinerary
            </p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title">Tell Us Your Preferences</h3>
                <p class="feature-desc">Share your travel style, budget, interests, and must-see destinations.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">AI Generates Your Plan</h3>
                <p class="feature-desc">Our advanced AI creates a custom travel plan tailored to your needs.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✈️</div>
                <h3 class="feature-title">Travel with Confidence</h3>
                <p class="feature-desc">Enjoy your perfectly planned journey with all details taken care of.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Why Choose Travelume Section
    st.markdown("""
    <div class="why-choose">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 2.5rem; color: #333 !important; margin-bottom: 20px;">Why Choose Travelume</h2>
            <p style="font-size: 1.2rem; color: #666 !important; max-width: 600px; margin: 0 auto;">
                Experience the future of travel planning
            </p>
        </div>
        <div class="why-choose-grid">
            <div class="why-choose-card">
                <div class="why-choose-number">1</div>
                <h3 class="why-choose-title">AI-Powered Planning</h3>
                <p class="why-choose-desc">
                    Advanced AI technology instantly generates smart, end-to-end itineraries tailored to your preferences.
                </p>
            </div>
            <div class="why-choose-card">
                <div class="why-choose-number">2</div>
                <h3 class="why-choose-title">Detailed Itineraries</h3>
                <p class="why-choose-desc">
                    Get day-by-day schedules, budget breakdowns, packing lists, and local tips for any destination.
                </p>
            </div>
            <div class="why-choose-card">
                <div class="why-choose-number">3</div>
                <h3 class="why-choose-title">Completely Free</h3>
                <p class="why-choose-desc">
                    No subscriptions, no hidden fees. Create unlimited travel plans without any payment required.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# AI PLANNER PAGE
elif st.session_state.current_page == 'ai_planner':
    if AI_PLANNER_AVAILABLE:
        render_ai_planner()
    else:
        st.error("AI Planner is not available. Please check if modules/ai_planner.py exists.")
        if st.button("Back to Home"):
            st.session_state.current_page = 'home'
            st.rerun()

# DESTINATIONS PAGE
elif st.session_state.current_page == 'destinations':
    create_destinations_page()

# ==================== ADDED: LOGIN/SIGNUP PAGE ====================
elif st.session_state.current_page == 'html_auth':
    show_auth_page()

# ==================== ADDED: ACCOUNT PAGE ====================
elif st.session_state.current_page == 'account':
    show_account_page()

# ==================== ADDED: HOTEL BOOKING PAGE ====================
elif st.session_state.current_page == 'hotel_booking':
    show_hotel_booking_page()

# ==================== ADDED: FLIGHT BOOKING PAGE ====================
elif st.session_state.current_page == 'flight_booking':  # ADDED THIS CONDITION
    show_flight_booking_page()

# DESTINATION ITINERARY PAGES
elif st.session_state.current_page == 'dubai_plan':
    create_dubai_plan_page()

elif st.session_state.current_page == 'thailand_plan':
    create_thailand_plan_page()

elif st.session_state.current_page == 'georgia_plan':
    create_georgia_plan_page()

elif st.session_state.current_page == 'maldives_plan':
    create_maldives_plan_page()

elif st.session_state.current_page == 'paris_plan':
    create_paris_plan_page()

elif st.session_state.current_page == 'bali_plan':
    create_bali_plan_page()

# SIDEBAR - Quick Navigation - UPDATED
with st.sidebar:
# Sidebar Chatbot removed in favor of floating popover
    st.markdown("---")

st.sidebar.markdown("## 🧭 Quick Navigation")

# Main navigation buttons
if st.sidebar.button("🏠 Home", key="sidebar_home", use_container_width=True):
    st.session_state.current_page = 'home'
    st.rerun()

if st.sidebar.button("🌍 Destinations", key="sidebar_destinations", use_container_width=True):
    st.session_state.current_page = 'destinations'
    st.rerun()

if st.sidebar.button("🤖 AI Planner", key="sidebar_ai", use_container_width=True):
    if AI_PLANNER_AVAILABLE:
        st.session_state.current_page = 'ai_planner'
        st.rerun()
    else:
        st.sidebar.error("AI Planner not available")

# Flights and Hotels removed from sidebar to declutter

# Show saved trips in sidebar if user is logged in
if st.session_state.authenticated:
    saved_trips = get_user_saved_trips()
    if saved_trips:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💼 My Saved Trips")
        for trip in saved_trips[:3]:  # Show first 3 trips
            trip_display_name = trip['name']
            if len(trip_display_name) > 20:
                trip_display_name = trip_display_name[:17] + "..."
            if st.sidebar.button(f"📍 {trip_display_name}", 
                                 key=f"sidebar_trip_{trip['id']}", use_container_width=True):
                st.session_state.current_page = 'account'
                st.session_state.account_tab = 'saved_trips'
                st.rerun()
        if len(saved_trips) > 3:
            if st.sidebar.button("View All Trips →", key="sidebar_view_all", use_container_width=True):
                st.session_state.current_page = 'account'
                st.session_state.account_tab = 'saved_trips'
                st.rerun()

# Quick Destinations removed to clean sidebar

# User info if logged in
if st.session_state.authenticated:
    st.sidebar.markdown("---")
    st.sidebar.success(f"✅ Welcome, {st.session_state.current_user['name']}!")
    
    # Show user stats
    try:
        from modules.database import get_database
        db = get_database()
        trips_count = len(saved_trips)
        journals_count = len(db.get_user_journals(st.session_state.current_user['email']))
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Trips", trips_count)
        with col2:
            st.metric("Journals", journals_count)
    except:
        pass
    
    if st.sidebar.button("My Account", key="sidebar_account", use_container_width=True):
        st.session_state.current_page = 'account'
        st.rerun()
    
    # Quick create journal button
    if st.sidebar.button("📝 Create Journal", key="sidebar_create_journal", use_container_width=True, type="secondary"):
        st.session_state.current_page = 'account'
        st.session_state.account_tab = 'my_journals'
        st.session_state.journal_action = 'create'
        st.rerun()
    
    # Quick book flight button
    if st.sidebar.button("✈️ Book Flight", key="sidebar_book_flight", use_container_width=True, type="secondary"):
        st.session_state.current_page = 'flight_booking'
        st.rerun()
    
    if st.sidebar.button("Logout", key="sidebar_logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.current_page = 'home'
        st.rerun()
else:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Account")
    col_sb1, col_sb2 = st.sidebar.columns(2)
    with col_sb1:
        if st.button("Sign Up", key="sidebar_signup", use_container_width=True):
            st.session_state.current_page = 'html_auth'
            st.rerun()
    with col_sb2:
        if st.button("Login", key="sidebar_login", use_container_width=True):
            st.session_state.current_page = 'html_auth'
            st.rerun()