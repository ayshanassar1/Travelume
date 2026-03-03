"""
UI components for agency display and interaction
"""

import streamlit as st
from modules.agency_fetcher import OSMAgencyFetcher
from modules.agency_database import AgencyDatabase

def show_agency_directory():
    """Main agency directory page"""
    st.title("🏢 Verified Travel Agencies")
    
    # Search section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        destination = st.text_input(
            "📍 Search agencies by destination",
            placeholder="e.g., Dubai, Thailand, Paris"
        )
    
    with col2:
        service_type = st.selectbox(
            "🔧 Service type",
            ["All", "visa_service", "air_tickets", "hotel_reservation", "package_tours"]
        )
    
    if st.button("🔍 Search Agencies", type="primary"):
        if destination:
            with st.spinner("Searching for travel agencies..."):
                fetcher = OSMAgencyFetcher()
                agencies = fetcher.search_by_destination(destination)
                
                if not agencies:
                    st.warning(f"No travel agencies found for {destination}")
                else:
                    show_agency_results(agencies, destination)
        else:
            st.warning("Please enter a destination")
    
    # Show verified agencies
    st.markdown("---")
    st.subheader("✅ Our Verified Partners")
    
    db = AgencyDatabase()
    verified_agencies = db.get_verified_agencies()
    
    if verified_agencies:
        show_verified_agencies_grid(verified_agencies)
    else:
        st.info("No verified agencies yet. Be the first to verify one!")

def show_agency_results(agencies, destination):
    """Display search results"""
    st.subheader(f"🏢 Travel Agencies in {destination}")
    st.caption(f"Found {len(agencies)} agencies (Data from OpenStreetMap)")
    
    for idx, agency in enumerate(agencies):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {agency['name']}")
                
                # Address
                if agency['full_address']:
                    st.markdown(f"📍 {agency['full_address']}")
                
                # Contact info
                contact_html = ""
                if agency['contact']['phone']:
                    contact_html += f"📞 {agency['contact']['phone']}  "
                if agency['contact']['website']:
                    contact_html += f"🌐 {agency['contact']['website']}  "
                if agency['contact']['email']:
                    contact_html += f"✉️ {agency['contact']['email']}"
                
                if contact_html:
                    st.markdown(contact_html)
                
                # Services
                if agency['services']:
                    services_str = " • ".join(agency['services'])
                    st.markdown(f"🛠️ **Services:** {services_str}")
            
            with col2:
                # Action buttons
                if st.button("📞 Contact", key=f"contact_{idx}"):
                    show_contact_form(agency)
                
                if st.button("✅ Verify", key=f"verify_{idx}", type="secondary"):
                    verify_agency_dialog(agency)
                
                if st.button("📌 Save", key=f"save_{idx}"):
                    save_agency_to_profile(agency)

def show_verified_agencies_grid(agencies):
    """Display verified agencies in a grid"""
    cols = st.columns(2)
    
    for idx, agency in enumerate(agencies[:6]):  # Show first 6
        with cols[idx % 2]:
            with st.container(border=True, height=250):
                st.markdown(f"##### 🏆 {agency['name']}")
                st.markdown(f"**📍** {agency.get('full_address', 'Address not available')}")
                
                if agency.get('verified_by'):
                    st.markdown(f"✅ Verified by: {agency['verified_by']}")
                
                # Services (truncated)
                services = agency.get('services', [])[:3]
                if services:
                    st.markdown(f"🛠️ {', '.join(services)}")
                
                # Contact button
                if st.button("Contact Agency", key=f"vcontact_{idx}", use_container_width=True):
                    show_contact_form(agency)

def show_contact_form(agency):
    """Show contact form for an agency"""
    st.session_state['contacting_agency'] = agency
    
    with st.form(key=f"contact_form_{agency['id']}"):
        st.subheader(f"Contact {agency['name']}")
        
        # Pre-fill with user info if logged in
        if st.session_state.get('authenticated'):
            user_name = st.session_state.current_user['name']
            user_email = st.session_state.current_user['email']
        else:
            user_name = st.text_input("Your Name")
            user_email = st.text_input("Your Email")
        
        trip_purpose = st.selectbox(
            "What do you need help with?",
            ["Flight Booking", "Hotel Reservation", "Visa Assistance", 
             "Tour Package", "Custom Itinerary", "Other"]
        )
        
        trip_details = st.text_area(
            "Trip Details",
            placeholder="Destination, dates, budget, number of people..."
        )
        
        preferred_contact = st.multiselect(
            "Preferred contact method",
            ["Email", "Phone", "WhatsApp"],
            default=["Email"]
        )
        
        urgency = st.slider("Urgency level", 1, 5, 3)
        
        submitted = st.form_submit_button("Send Request")
        
        if submitted:
            # Save request to database
            save_contact_request(
                agency=agency,
                user_info={"name": user_name, "email": user_email},
                purpose=trip_purpose,
                details=trip_details,
                contact_methods=preferred_contact,
                urgency=urgency
            )
            
            st.success(f"✅ Request sent to {agency['name']}! They'll contact you within 24 hours.")

def verify_agency_dialog(agency):
    """Dialog for admin to verify an agency"""
    if not st.session_state.get('authenticated'):
        st.warning("Please login as admin to verify agencies")
        return
    
    # Check if user is admin (simple check for now)
    user_email = st.session_state.current_user['email']
    
    with st.form(key=f"verify_form_{agency['id']}"):
        st.subheader(f"Verify {agency['name']}")
        
        verification_method = st.selectbox(
            "Verification method",
            ["Phone Call", "Email Verification", "Document Check", 
             "Website Verification", "In-person Visit"]
        )
        
        verification_notes = st.text_area("Verification Notes")
        
        contact_verified = st.checkbox("Contact information verified")
        services_verified = st.checkbox("Services verified")
        license_verified = st.checkbox("Business license verified (if applicable)")
        
        trust_score = st.slider("Trust Score", 0, 100, 80)
        
        if st.form_submit_button("Mark as Verified"):
            if contact_verified and services_verified:
                db = AgencyDatabase()
                agency_id = db.add_verified_agency(
                    agency, 
                    verified_by=user_email,
                    verification_notes=verification_notes
                )
                st.success(f"✅ Agency verified! ID: {agency_id}")
                st.rerun()
            else:
                st.error("Please verify at least contact and services")

def save_agency_to_profile(agency):
    """Save agency to user's profile"""
    if not st.session_state.get('authenticated'):
        st.warning("Please login to save agencies")
        return
    
    user_email = st.session_state.current_user['email']
    
    # Create user agencies file if not exists
    user_agencies_file = f"data/user_agencies_{user_email}.json"
    
    if not os.path.exists(user_agencies_file):
        with open(user_agencies_file, 'w') as f:
            json.dump({"saved_agencies": []}, f, indent=2)
    
    with open(user_agencies_file, 'r') as f:
        data = json.load(f)
    
    # Check if already saved
    for saved in data['saved_agencies']:
        if saved.get('id') == agency['id']:
            st.info("Agency already saved to your profile")
            return
    
    # Add to saved agencies
    data['saved_agencies'].append({
        **agency,
        'saved_date': datetime.now().isoformat(),
        'notes': ""
    })
    
    with open(user_agencies_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    st.success(f"✅ {agency['name']} saved to your profile!")

def save_contact_request(agency, user_info, purpose, details, contact_methods, urgency):
    """Save contact request to database"""
    requests_file = "data/contact_requests.json"
    
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(requests_file):
        with open(requests_file, 'w') as f:
            json.dump({"requests": []}, f, indent=2)
    
    with open(requests_file, 'r') as f:
        data = json.load(f)
    
    request_id = f"REQ_{int(datetime.now().timestamp())}"
    
    request = {
        'request_id': request_id,
        'agency_id': agency['id'],
        'agency_name': agency['name'],
        'user_info': user_info,
        'purpose': purpose,
        'details': details,
        'contact_methods': contact_methods,
        'urgency': urgency,
        'status': 'pending',
        'date_submitted': datetime.now().isoformat(),
        'date_contacted': None,
        'notes': ""
    }
    
    data['requests'].append(request)
    
    with open(requests_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return request_id