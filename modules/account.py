"""
Account Module for Travelume
Handles user account management and profile display
Integrated with Journal module
"""

import streamlit as st
from datetime import datetime
from modules.database import get_database
from modules.journal import show_journals_page  # Import the journals module

def show_account_page(user_data):
    """Display the account page with user information and options"""
    
    # Initialize session state for active tab
    if 'account_tab' not in st.session_state:
        st.session_state.account_tab = "profile"
    
    # Page header
    st.title("👤 My Account")
    
    # Welcome message
    col_welcome, col_logout = st.columns([3, 1])
    with col_welcome:
        st.markdown(f"### Welcome back, {user_data.get('name', 'User')}!")
    with col_logout:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # User info box
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("---")
            st.markdown(f"**Name:** {user_data.get('name', 'Not set')}")
            st.markdown(f"**Email:** {user_data.get('email', 'Not set')}")
            st.markdown(f"**Member since:** {user_data.get('created_at', 'Unknown')}")
            
            # Statistics
            db = get_database()
            user_trips = db.get_user_trips(user_data['email'])
            user_journals = db.get_user_journals(user_data['email'])
            
            st.markdown("---")
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("Total Trips", len(user_trips))
            with col_stats2:
                st.metric("Travel Journals", len(user_journals))
            st.markdown("---")
    
    # Navigation tabs
    tabs = ["📋 Profile", "🗺️ Saved Trips", "📚 My Journals"]
    
    # Create tabs
    col1, col2, col3 = st.columns(3)
    tab_cols = [col1, col2, col3]
    
    for idx, tab_name in enumerate(tabs):
        with tab_cols[idx]:
            is_active = st.session_state.account_tab == tab_name.lower().replace(" ", "_")
            button_type = "primary" if is_active else "secondary"
            
            if st.button(tab_name, key=f"tab_{idx}", type=button_type, use_container_width=True):
                st.session_state.account_tab = tab_name.lower().replace(" ", "_")
                st.rerun()
    
    st.markdown("---")
    
    # Display content based on selected tab
    if st.session_state.account_tab == "profile":
        _show_profile_tab(user_data)
    elif st.session_state.account_tab == "saved_trips":
        _show_trips_tab(user_data)
    elif st.session_state.account_tab == "my_journals":
        _show_journals_tab(user_data)

def _show_profile_tab(user_data):
    """Display profile editing options"""
    st.header("📋 Profile Settings")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name", 
                                    value=user_data.get('name', ''),
                                    placeholder="Enter your full name")
            
            # Preferences
            st.subheader("Preferences")
            theme = st.selectbox("Theme", 
                                ["Light", "Dark", "Auto"],
                                index=["Light", "Dark", "Auto"].index(
                                    user_data.get('preferences', {}).get('theme', 'Light')
                                ) if user_data.get('preferences', {}).get('theme', 'Light') in ["Light", "Dark", "Auto"] else 0)
            
            budget_range = st.selectbox("Budget Range",
                                       ["Budget", "Moderate", "Luxury", "Not set"],
                                       index=["Budget", "Moderate", "Luxury", "Not set"].index(
                                           user_data.get('preferences', {}).get('budget_range', 'Not set')
                                       ) if user_data.get('preferences', {}).get('budget_range', 'Not set') in ["Budget", "Moderate", "Luxury", "Not set"] else 3)
        
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
                default=user_data.get('preferences', {}).get('travel_style', [])
            )
        
        # Submit button
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            submit = st.form_submit_button("💾 Save Changes", type="primary")
        with col_btn2:
            if st.form_submit_button("❌ Cancel"):
                pass
        
        if submit:
            db = get_database()
            updates = {}
            
            # Update name if changed
            if new_name and new_name != user_data.get('name'):
                updates['name'] = new_name
            
            # Update preferences
            preferences = user_data.get('preferences', {}).copy()
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
                    user_with_pass = db.authenticate_user(user_data['email'], current_password)
                    if user_with_pass:
                        if db.update_user_password(user_data['email'], new_password):
                            password_changed = True
                            st.success("✅ Password updated successfully!")
                    else:
                        st.error("Current password is incorrect")
                else:
                    st.error("New passwords don't match")
            
            # Apply other updates
            if updates:
                if db.update_user(user_data['email'], **updates):
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
            
            if not updates and not password_changed:
                st.info("No changes made to your profile.")

def _show_trips_tab(user_data):
    """Display saved trips"""
    st.header("🗺️ My Saved Trips")
    
    db = get_database()
    user_trips = db.get_user_trips(user_data['email'])
    
    if not user_trips:
        st.info("You haven't saved any trips yet.")
        st.markdown("""
        Plan your next adventure with our AI Planner!
        
        - ✨ **AI Trip Planning**: Get personalized itineraries
        - 🗺️ **Destination Ideas**: Discover new places to explore
        - 💰 **Budget Planning**: Stay within your budget
        - ⏱️ **Time Optimization**: Make the most of your time
        
        Click on **AI Planner** in the navigation to get started!
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to AI Planner", type="primary"):
                # You'll need to set navigation state based on your app structure
                st.success("Navigate to AI Planner (implementation depends on your navigation)")
        return
    
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search trips", placeholder="Search by destination or title")
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest", "Destination A-Z", "Budget", "Duration"])
    
    # Filter trips
    filtered_trips = user_trips
    
    if search_query:
        filtered_trips = [
            trip for trip in filtered_trips 
            if search_query.lower() in trip.get('destination', '').lower() 
            or search_query.lower() in trip.get('title', '').lower()
        ]
    
    # Sort trips
    if sort_by == "Newest":
        filtered_trips.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_by == "Destination A-Z":
        filtered_trips.sort(key=lambda x: x.get('destination', '').lower())
    elif sort_by == "Budget":
        filtered_trips.sort(key=lambda x: x.get('total_budget', 0))
    elif sort_by == "Duration":
        filtered_trips.sort(key=lambda x: x.get('duration_days', 0))
    
    # Display trips
    for trip in filtered_trips:
        _display_trip_card(trip)

def _display_trip_card(trip):
    """Display a trip card"""
    trip_id = trip.get('id')
    destination = trip.get('destination', 'Unknown Destination')
    title = trip.get('title', 'Untitled Trip')
    duration = trip.get('duration_days', 0)
    budget = trip.get('total_budget', 0)
    created_date = trip.get('created_at', '')
    
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Display trip image if available
            image_url = trip.get('image_url')
            if image_url:
                st.image(image_url, use_column_width=True)
            else:
                st.image("https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=400", 
                        caption=destination, use_column_width=True)
        
        with col2:
            st.subheader(destination)
            st.caption(f"🗓️ {duration} days | 💰 ₹{budget:,} | 📅 {created_date}")
            
            if title and title != destination:
                st.write(f"**{title}**")
            
            # Display itinerary highlights
            itinerary = trip.get('itinerary', [])
            if itinerary and len(itinerary) > 0:
                with st.expander("View Itinerary Highlights"):
                    for day in itinerary[:3]:  # Show first 3 days
                        st.write(f"**Day {day.get('day', '?')}:** {day.get('title', '')}")
                        if len(itinerary) > 3:
                            st.write(f"... and {len(itinerary) - 3} more days")
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("📖 View Details", key=f"view_trip_{trip_id}", use_container_width=True):
                    st.session_state.view_trip = trip_id
                    # You'll need to implement trip detail view based on your app structure
            
            with col_btn2:
                # Button to create journal from this trip
                if st.button("📝 Create Journal", key=f"journal_trip_{trip_id}", use_container_width=True):
                    st.session_state.account_tab = "my_journals"
                    st.session_state.journal_action = "create"
                    st.session_state.linked_trip_id = trip_id
                    st.rerun()
            
            with col_btn3:
                if st.button("🗑️ Delete", key=f"delete_trip_{trip_id}", 
                            type="secondary", use_container_width=True):
                    # Confirm deletion
                    if st.session_state.get(f"confirm_delete_{trip_id}"):
                        db = get_database()
                        if db.delete_trip(st.session_state.user_email, trip_id):
                            st.success("Trip deleted!")
                            st.rerun()
                    else:
                        st.session_state[f"confirm_delete_{trip_id}"] = True
                        st.warning("Click delete again to confirm")
                        st.rerun()
        
        st.divider()

def _show_journals_tab(user_data):
    """Display the journals interface"""
    st.header("📚 My Travel Journals")
    
    # Introduction
    st.markdown("""
    Your personal travel diary! Create beautiful journals from your trips with photos, stories, and memories.
    
    **Features:**
    - 📸 **Upload photos** from your travels
    - 📝 **Write stories** and memories
    - 📄 **Generate PDFs** for keepsakes
    - 🏷️ **Add tags** to organize journals
    - 🔗 **Link to trips** for context
    
    Create your first journal to preserve your travel memories!
    """)
    
    # Show the journals page from journal module
    show_journals_page(user_data['email'])

def show_account_section(user_data):
    """Compact account display for sidebar or header"""
    if not user_data:
        return
    
    with st.container():
        st.markdown(f"### 👤 {user_data.get('name', 'User')}")
        st.markdown(f"✉️ {user_data.get('email', '')}")
        
        # Quick stats
        db = get_database()
        trips_count = len(db.get_user_trips(user_data['email']))
        journals_count = len(db.get_user_journals(user_data['email']))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Trips", trips_count)
        with col2:
            st.metric("Journals", journals_count)
        
        # Quick actions
        st.markdown("---")
        if st.button("📋 Go to My Account", use_container_width=True):
            st.session_state.current_page = "account"
            st.rerun()
        
        if st.button("📝 Create Journal", type="secondary", use_container_width=True):
            st.session_state.current_page = "account"
            st.session_state.account_tab = "my_journals"
            st.session_state.journal_action = "create"
            st.rerun()

# Test function
def test_account_module():
    """Test the account module"""
    st.title("Account Module Test")
    
    # Mock user data for testing
    test_user = {
        'email': 'test@example.com',
        'name': 'Test User',
        'created_at': '2024-01-01 10:00:00',
        'preferences': {
            'theme': 'Light',
            'budget_range': 'Moderate',
            'travel_style': ['Adventure', 'Cultural']
        }
    }
    
    if 'test_user' not in st.session_state:
        st.session_state.user_email = test_user['email']
        st.session_state.user_data = test_user
    
    show_account_page(test_user)

if __name__ == "__main__":
    test_account_module()