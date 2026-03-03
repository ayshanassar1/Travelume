"""
Flight Booking Module for Travelume
Handles flight search, booking, and integration with itineraries
"""

import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

class FlightBooking:
    """Flight booking system with mock/flight API integration"""
    
    def __init__(self):
        # Mock flight data
        self.airlines = [
            "Air India", "IndiGo", "SpiceJet", "Vistara", "AirAsia India",
            "Emirates", "Qatar Airways", "Singapore Airlines", "Etihad Airways",
            "British Airways", "Lufthansa", "Turkish Airlines"
        ]
        
        self.mock_flights = self._load_mock_flights()
        
        # Flight classes
        self.flight_classes = {
            "Economy": {"icon": "💺", "price_multiplier": 1.0},
            "Premium Economy": {"icon": "🪑", "price_multiplier": 1.5},
            "Business": {"icon": "🛋️", "price_multiplier": 2.5},
            "First Class": {"icon": "🛌", "price_multiplier": 4.0}
        }
        
    def _load_mock_flights(self):
        """Load mock flight data"""
        return [
            {
                "id": "AI-202",
                "airline": "Air India",
                "flight_number": "AI-202",
                "from": "DEL",
                "to": "DXB",
                "departure_time": "02:30",
                "arrival_time": "05:15",
                "duration": "3h 45m",
                "price": 18500,
                "stops": 0,
                "aircraft": "Boeing 787-8",
                "baggage": "25kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "EK-512",
                "airline": "Emirates",
                "flight_number": "EK-512",
                "from": "BOM",
                "to": "DXB",
                "departure_time": "08:45",
                "arrival_time": "10:30",
                "duration": "3h 45m",
                "price": 22500,
                "stops": 0,
                "aircraft": "Airbus A380",
                "baggage": "30kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "6E-108",
                "airline": "IndiGo",
                "flight_number": "6E-108",
                "from": "DEL",
                "to": "BKK",
                "departure_time": "14:20",
                "arrival_time": "19:45",
                "duration": "4h 25m",
                "price": 15600,
                "stops": 0,
                "aircraft": "Airbus A320neo",
                "baggage": "15kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "SG-87",
                "airline": "SpiceJet",
                "flight_number": "SG-87",
                "from": "BLR",
                "to": "SIN",
                "departure_time": "22:10",
                "arrival_time": "05:30+1",
                "duration": "5h 20m",
                "price": 18900,
                "stops": 0,
                "aircraft": "Boeing 737-800",
                "baggage": "20kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "QR-578",
                "airline": "Qatar Airways",
                "flight_number": "QR-578",
                "from": "DEL",
                "to": "CDG",
                "departure_time": "01:40",
                "arrival_time": "11:20",
                "duration": "9h 40m",
                "price": 48500,
                "stops": 1,
                "aircraft": "Boeing 777-300ER",
                "baggage": "35kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "SQ-402",
                "airline": "Singapore Airlines",
                "flight_number": "SQ-402",
                "from": "MAA",
                "to": "SIN",
                "departure_time": "20:15",
                "arrival_time": "04:45+1",
                "duration": "4h 30m",
                "price": 17800,
                "stops": 0,
                "aircraft": "Airbus A350",
                "baggage": "30kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "UK-980",
                "airline": "Vistara",
                "flight_number": "UK-980",
                "from": "DEL",
                "to": "BOM",
                "departure_time": "07:30",
                "arrival_time": "09:45",
                "duration": "2h 15m",
                "price": 6500,
                "stops": 0,
                "aircraft": "Airbus A321neo",
                "baggage": "25kg",
                "departure_date": "2024-06-15"
            },
            {
                "id": "I5-762",
                "airline": "AirAsia India",
                "flight_number": "I5-762",
                "from": "DEL",
                "to": "GOI",
                "departure_time": "11:20",
                "arrival_time": "14:05",
                "duration": "2h 45m",
                "price": 4200,
                "stops": 0,
                "aircraft": "Airbus A320",
                "baggage": "15kg",
                "departure_date": "2024-06-15"
            }
        ]
    
    def search_flights(self, from_city: str, to_city: str, departure_date: str, 
                      passengers: int = 1, flight_class: str = "Economy") -> List[Dict]:
        """Search for flights based on criteria"""
        # In a real app, this would call an API
        # For now, return filtered mock data
        
        filtered_flights = []
        for flight in self.mock_flights:
            # Simple matching logic (in real app, use proper city-to-airport mapping)
            if from_city.lower() in flight["from"].lower() or flight["from"].lower() in from_city.lower():
                if to_city.lower() in flight["to"].lower() or flight["to"].lower() in to_city.lower():
                    # Apply class multiplier to price
                    flight_copy = flight.copy()
                    class_multiplier = self.flight_classes.get(flight_class, {}).get("price_multiplier", 1.0)
                    flight_copy["price"] = int(flight_copy["price"] * class_multiplier * passengers)
                    flight_copy["passengers"] = passengers
                    flight_copy["class"] = flight_class
                    filtered_flights.append(flight_copy)
        
        return filtered_flights
    
    def get_city_suggestions(self, query: str) -> List[Dict]:
        """Get city/airport suggestions for autocomplete"""
        airports = [
            {"code": "DEL", "name": "Delhi", "country": "India", "full_name": "Delhi (DEL) - Indira Gandhi International"},
            {"code": "BOM", "name": "Mumbai", "country": "India", "full_name": "Mumbai (BOM) - Chhatrapati Shivaji Maharaj International"},
            {"code": "BLR", "name": "Bengaluru", "country": "India", "full_name": "Bengaluru (BLR) - Kempegowda International"},
            {"code": "MAA", "name": "Chennai", "country": "India", "full_name": "Chennai (MAA) - Chennai International"},
            {"code": "HYD", "name": "Hyderabad", "country": "India", "full_name": "Hyderabad (HYD) - Rajiv Gandhi International"},
            {"code": "CCU", "name": "Kolkata", "country": "India", "full_name": "Kolkata (CCU) - Netaji Subhash Chandra Bose International"},
            {"code": "GOI", "name": "Goa", "country": "India", "full_name": "Goa (GOI) - Dabolim Airport"},
            
            {"code": "DXB", "name": "Dubai", "country": "UAE", "full_name": "Dubai (DXB) - Dubai International"},
            {"code": "BKK", "name": "Bangkok", "country": "Thailand", "full_name": "Bangkok (BKK) - Suvarnabhumi Airport"},
            {"code": "SIN", "name": "Singapore", "country": "Singapore", "full_name": "Singapore (SIN) - Changi Airport"},
            {"code": "KUL", "name": "Kuala Lumpur", "country": "Malaysia", "full_name": "Kuala Lumpur (KUL) - Kuala Lumpur International"},
            {"code": "HKT", "name": "Phuket", "country": "Thailand", "full_name": "Phuket (HKT) - Phuket International"},
            {"code": "CDG", "name": "Paris", "country": "France", "full_name": "Paris (CDG) - Charles de Gaulle"},
            {"code": "LHR", "name": "London", "country": "UK", "full_name": "London (LHR) - Heathrow"},
            {"code": "JFK", "name": "New York", "country": "USA", "full_name": "New York (JFK) - John F. Kennedy"},
            {"code": "SYD", "name": "Sydney", "country": "Australia", "full_name": "Sydney (SYD) - Kingsford Smith"},
            {"code": "NRT", "name": "Tokyo", "country": "Japan", "full_name": "Tokyo (NRT) - Narita International"},
            {"code": "ICN", "name": "Seoul", "country": "South Korea", "full_name": "Seoul (ICN) - Incheon International"},
        ]
        
        suggestions = []
        query_lower = query.lower()
        
        for airport in airports:
            if (query_lower in airport["name"].lower() or 
                query_lower in airport["code"].lower() or
                query_lower in airport["country"].lower() or
                query_lower in airport["full_name"].lower()):
                suggestions.append(airport)
        
        return suggestions[:10]  # Limit to 10 suggestions
    
    def book_flight(self, flight_id: str, passenger_details: Dict) -> Dict:
        """Mock flight booking function"""
        # In real app, this would call booking API
        booking_id = f"FLT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Find the flight
        flight = next((f for f in self.mock_flights if f["id"] == flight_id), None)
        
        if not flight:
            return {"success": False, "message": "Flight not found"}
        
        booking_details = {
            "booking_id": booking_id,
            "flight": flight,
            "passenger_details": passenger_details,
            "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Confirmed",
            "pnr": f"PNR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "total_amount": flight["price"],
            "payment_status": "Pending"
        }
        
        # Save booking (in real app, save to database)
        self._save_booking(booking_details)
        
        return {
            "success": True,
            "booking_id": booking_id,
            "message": f"Flight booking confirmed! Your PNR is {booking_details['pnr']}",
            "details": booking_details
        }
    
    def _save_booking(self, booking_details: Dict):
        """Save booking to JSON file"""
        try:
            bookings_file = "data/flight_bookings.json"
            
            # Create directory if it doesn't exist
            os.makedirs("data", exist_ok=True)
            
            # Load existing bookings
            if os.path.exists(bookings_file):
                with open(bookings_file, 'r') as f:
                    bookings = json.load(f)
            else:
                bookings = []
            
            # Add new booking
            bookings.append(booking_details)
            
            # Save back to file
            with open(bookings_file, 'w') as f:
                json.dump(bookings, f, indent=2)
                
        except Exception as e:
            st.error(f"Error saving booking: {e}")
    
    def get_user_bookings(self, user_email: str) -> List[Dict]:
        """Get flight bookings for a user"""
        try:
            bookings_file = "data/flight_bookings.json"
            
            if not os.path.exists(bookings_file):
                return []
            
            with open(bookings_file, 'r') as f:
                all_bookings = json.load(f)
            
            # Filter by user email (in real app, associate bookings with user)
            user_bookings = []
            for booking in all_bookings:
                if booking.get("passenger_details", {}).get("email") == user_email:
                    user_bookings.append(booking)
            
            return user_bookings
            
        except Exception as e:
            st.error(f"Error loading bookings: {e}")
            return []
    
    def display_flight_card(self, flight: Dict, show_book_button: bool = True):
        """Display a flight card with details"""
        with st.container(border=True):
            # Flight header
            col1, col2, col3 = st.columns([2, 3, 2])
            
            with col1:
                st.markdown(f"### {flight['airline']}")
                st.markdown(f"**{flight['flight_number']}**")
                st.caption(flight['aircraft'])
            
            with col2:
                # Route and timing
                col_time1, col_arrow, col_time2 = st.columns([2, 1, 2])
                
                with col_time1:
                    st.markdown(f"**{flight['departure_time']}**")
                    st.markdown(f"**{flight['from']}**")
                
                with col_arrow:
                    st.markdown("<div style='text-align: center;'>→</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center;'>{flight['duration']}</div>", unsafe_allow_html=True)
                    if flight['stops'] > 0:
                        st.caption(f"{flight['stops']} stop{'s' if flight['stops'] > 1 else ''}")
                    else:
                        st.caption("Non-stop")
                
                with col_time2:
                    st.markdown(f"**{flight['arrival_time']}**")
                    st.markdown(f"**{flight['to']}**")
            
            with col3:
                # Price and booking
                st.markdown(f"### ₹{flight['price']: ,}")
                st.caption(f"For {flight.get('passengers', 1)} passenger{'s' if flight.get('passengers', 1) > 1 else ''}")
                st.caption(f"Class: {flight.get('class', 'Economy')}")
                
                if show_book_button:
                    if st.button("Book Now", key=f"book_{flight['id']}", use_container_width=True):
                        st.session_state.selected_flight = flight
                        st.session_state.flight_booking_step = "passenger_details"
                        st.rerun()
            
            # Additional details in expander
            with st.expander("Flight Details"):
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown(f"**Departure Date:** {flight.get('departure_date', 'N/A')}")
                    st.markdown(f"**Baggage Allowance:** {flight.get('baggage', 'N/A')}")
                with col_info2:
                    st.markdown(f"**Stops:** {flight['stops']}")
                    if "cancellation_policy" in flight:
                        st.markdown(f"**Cancellation:** {flight['cancellation_policy']}")
                    else:
                        st.markdown("**Cancellation:** Flexible (Free cancellation up to 24 hours)")
    
    def display_passenger_form(self, flight: Dict):
        """Display passenger details form"""
        st.markdown(f"### ✈️ Booking: {flight['airline']} {flight['flight_number']}")
        st.markdown(f"**Route:** {flight['from']} → {flight['to']} | **Date:** {flight.get('departure_date', 'N/A')}")
        st.markdown(f"**Total Fare:** ₹{flight['price']: ,}")
        
        with st.form("passenger_form"):
            st.subheader("Passenger Details")
            
            # Passenger count
            passenger_count = flight.get('passengers', 1)
            
            # Create fields for each passenger
            passengers = []
            for i in range(passenger_count):
                st.markdown(f"#### Passenger {i+1}")
                
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input(f"First Name {i+1}", key=f"first_name_{i}")
                    gender = st.selectbox(f"Gender {i+1}", ["Male", "Female", "Other"], key=f"gender_{i}")
                    passport = st.text_input(f"Passport Number {i+1}", key=f"passport_{i}")
                
                with col2:
                    last_name = st.text_input(f"Last Name {i+1}", key=f"last_name_{i}")
                    dob = st.date_input(f"Date of Birth {i+1}", 
                                      min_value=datetime(1900, 1, 1),
                                      max_value=datetime.today(),
                                      key=f"dob_{i}")
                    nationality = st.text_input(f"Nationality {i+1}", value="Indian", key=f"nationality_{i}")
                
                passengers.append({
                    "first_name": first_name,
                    "last_name": last_name,
                    "gender": gender,
                    "dob": dob.strftime("%Y-%m-%d") if dob else "",
                    "passport": passport,
                    "nationality": nationality
                })
            
            # Contact details
            st.subheader("Contact Information")
            col_contact1, col_contact2 = st.columns(2)
            with col_contact1:
                email = st.text_input("Email Address", key="contact_email")
                phone = st.text_input("Phone Number", key="contact_phone")
            with col_contact2:
                address = st.text_area("Address", key="contact_address")
                emergency_contact = st.text_input("Emergency Contact", key="emergency_contact")
            
            # Payment method
            st.subheader("Payment Method")
            payment_method = st.selectbox(
                "Select Payment Method",
                ["Credit/Debit Card", "Net Banking", "UPI", "Wallet", "Cash on Delivery"],
                key="payment_method"
            )
            
            # Terms and conditions
            agreed = st.checkbox("I agree to the terms and conditions", key="terms_agree")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("✅ Confirm Booking", type="primary", use_container_width=True)
            with col_btn2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if cancel:
                st.session_state.flight_booking_step = "search"
                st.rerun()
            
            if submit:
                if not all([p["first_name"] for p in passengers]):
                    st.error("Please fill all passenger details")
                elif not email or not phone:
                    st.error("Please provide contact information")
                elif not agreed:
                    st.error("Please agree to terms and conditions")
                else:
                    # Prepare booking data
                    passenger_details = {
                        "passengers": passengers,
                        "contact": {
                            "email": email,
                            "phone": phone,
                            "address": address,
                            "emergency_contact": emergency_contact
                        },
                        "payment_method": payment_method
                    }
                    
                    # Make booking
                    with st.spinner("Processing your booking..."):
                        result = self.book_flight(flight["id"], passenger_details)
                        
                        if result["success"]:
                            st.success(result["message"])
                            st.balloons()
                            
                            # Show booking details
                            with st.expander("Booking Details"):
                                booking = result["details"]
                                st.json(booking)
                            
                            # Reset to search
                            st.session_state.flight_booking_step = "search"
                            st.session_state.selected_flight = None
                            
                            # Add a button to view bookings
                            if st.button("View My Bookings"):
                                st.session_state.flight_booking_step = "my_bookings"
                                st.rerun()
                        else:
                            st.error(result["message"])

def show_flight_booking_page():
    """Main function to show the flight booking page"""
    
    # Initialize session state for flight booking
    if 'flight_booking_step' not in st.session_state:
        st.session_state.flight_booking_step = "search"
    if 'selected_flight' not in st.session_state:
        st.session_state.selected_flight = None
    
    # Create flight booking instance
    flight_booker = FlightBooking()
    
    # Page header
    st.title("✈️ Flight Booking")
    st.markdown("Find and book flights to your dream destinations")
    
    # Show appropriate step
    if st.session_state.flight_booking_step == "search":
        _show_flight_search(flight_booker)
    elif st.session_state.flight_booking_step == "passenger_details" and st.session_state.selected_flight:
        flight_booker.display_passenger_form(st.session_state.selected_flight)
    elif st.session_state.flight_booking_step == "my_bookings":
        _show_my_bookings(flight_booker)

def _show_flight_search(flight_booker: FlightBooking):
    """Show flight search interface"""
    
    # Search form
    with st.container(border=True):
        st.subheader("🔍 Search Flights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # From city with autocomplete
            from_query = st.text_input("From", placeholder="City or Airport", key="from_city")
            if from_query:
                suggestions = flight_booker.get_city_suggestions(from_query)
                if suggestions:
                    with st.expander("Suggestions", expanded=True):
                        for suggestion in suggestions:
                            if st.button(f"📍 {suggestion['full_name']}", 
                                        key=f"from_{suggestion['code']}",
                                        use_container_width=True):
                                st.session_state.from_city = suggestion['full_name']
                                st.rerun()
        
        with col2:
            # To city with autocomplete
            to_query = st.text_input("To", placeholder="City or Airport", key="to_city")
            if to_query:
                suggestions = flight_booker.get_city_suggestions(to_query)
                if suggestions:
                    with st.expander("Suggestions", expanded=True):
                        for suggestion in suggestions:
                            if st.button(f"📍 {suggestion['full_name']}", 
                                        key=f"to_{suggestion['code']}",
                                        use_container_width=True):
                                st.session_state.to_city = suggestion['full_name']
                                st.rerun()
        
        with col3:
            # Date
            departure_date = st.date_input(
                "Departure Date",
                min_value=datetime.today(),
                value=datetime.today() + timedelta(days=30)
            )
    
    # Additional search options
    with st.expander("Advanced Options"):
        col4, col5, col6 = st.columns(3)
        
        with col4:
            passengers = st.number_input("Passengers", min_value=1, max_value=10, value=1)
        
        with col5:
            flight_class = st.selectbox(
                "Class",
                list(flight_booker.flight_classes.keys()),
                format_func=lambda x: f"{flight_booker.flight_classes[x]['icon']} {x}"
            )
        
        with col6:
            # Sort by
            sort_by = st.selectbox(
                "Sort by",
                ["Price: Low to High", "Price: High to Low", "Duration: Shortest", "Departure Time"]
            )
    
    # Search button
    if st.button("🔍 Search Flights", type="primary", use_container_width=True):
        with st.spinner("Searching for flights..."):
            # Get search values
            from_city = st.session_state.get('from_city', from_query) or from_query
            to_city = st.session_state.get('to_city', to_query) or to_query
            
            if not from_city or not to_city:
                st.error("Please enter both departure and destination cities")
            else:
                # Search flights
                flights = flight_booker.search_flights(
                    from_city=from_city,
                    to_city=to_city,
                    departure_date=departure_date.strftime("%Y-%m-%d"),
                    passengers=passengers,
                    flight_class=flight_class
                )
                
                # Store in session state
                st.session_state.search_results = flights
                st.session_state.search_params = {
                    "from_city": from_city,
                    "to_city": to_city,
                    "departure_date": departure_date,
                    "passengers": passengers,
                    "flight_class": flight_class
                }
    
    # Show search results if available
    if 'search_results' in st.session_state and st.session_state.search_results:
        st.markdown("---")
        st.subheader("📋 Available Flights")
        
        # Show search summary
        params = st.session_state.search_params
        st.info(f"**Search:** {params['from_city']} → {params['to_city']} | "
                f"**Date:** {params['departure_date'].strftime('%d %b %Y')} | "
                f"**Passengers:** {params['passengers']} | "
                f"**Class:** {params['flight_class']}")
        
        # Sort results
        flights = st.session_state.search_results
        if params.get('sort_by', 'Price: Low to High') == "Price: Low to High":
            flights.sort(key=lambda x: x["price"])
        elif params.get('sort_by') == "Price: High to Low":
            flights.sort(key=lambda x: x["price"], reverse=True)
        elif params.get('sort_by') == "Duration: Shortest":
            # Parse duration string to minutes
            def parse_duration(duration_str):
                parts = duration_str.split()
                total_minutes = 0
                for part in parts:
                    if 'h' in part:
                        total_minutes += int(part.replace('h', '')) * 60
                    elif 'm' in part:
                        total_minutes += int(part.replace('m', ''))
                return total_minutes
            
            flights.sort(key=lambda x: parse_duration(x["duration"]))
        
        # Display flights
        for flight in flights:
            flight_booker.display_flight_card(flight)
        
        if not flights:
            st.warning("No flights found for your search criteria. Try different dates or cities.")
    elif 'search_results' in st.session_state:
        st.warning("No flights found for your search criteria. Try different dates or cities.")
    
    # My Bookings button
    st.markdown("---")
    col_view1, col_view2 = st.columns(2)
    with col_view1:
        if st.session_state.get('authenticated'):
            if st.button("📋 View My Bookings", use_container_width=True):
                st.session_state.flight_booking_step = "my_bookings"
                st.rerun()
        else:
            st.info("Login to view your bookings")
    
    with col_view2:
        if st.button("🔄 New Search", use_container_width=True):
            for key in ['search_results', 'search_params', 'from_city', 'to_city']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def _show_my_bookings(flight_booker: FlightBooking):
    """Show user's flight bookings"""
    if not st.session_state.get('authenticated'):
        st.error("Please login to view your bookings")
        if st.button("Go to Login"):
            st.session_state.current_page = 'html_auth'
            st.rerun()
        return
    
    st.subheader("📋 My Flight Bookings")
    
    # Get user bookings
    user_email = st.session_state.current_user['email']
    bookings = flight_booker.get_user_bookings(user_email)
    
    if not bookings:
        st.info("You haven't made any flight bookings yet.")
        st.markdown("""
        Book your first flight to:
        - ✈️ **Save up to 30%** with early bird discounts
        - 🎫 **Flexible dates** for best prices
        - 🔒 **Secure booking** with instant confirmation
        - 📱 **Easy management** of all your bookings
        """)
        
        if st.button("Search Flights", type="primary"):
            st.session_state.flight_booking_step = "search"
            st.rerun()
        return
    
    # Display bookings
    for booking in bookings:
        with st.container(border=True):
            col_header1, col_header2, col_header3 = st.columns([3, 2, 1])
            
            with col_header1:
                flight = booking.get('flight', {})
                st.markdown(f"### {flight.get('airline', 'Unknown')} {flight.get('flight_number', '')}")
                st.markdown(f"**Route:** {flight.get('from', '')} → {flight.get('to', '')}")
            
            with col_header2:
                st.markdown(f"**Booking ID:** {booking.get('booking_id', '')}")
                st.markdown(f"**PNR:** {booking.get('pnr', '')}")
                status = booking.get('status', 'Confirmed')
                status_color = "green" if status == "Confirmed" else "orange" if status == "Pending" else "red"
                st.markdown(f"**Status:** <span style='color:{status_color};'>{status}</span>", unsafe_allow_html=True)
            
            with col_header3:
                st.markdown(f"### ₹{booking.get('total_amount', 0): ,}")
                st.caption(f"Booked: {booking.get('booking_time', '')}")
            
            # Booking details
            with st.expander("View Details"):
                col_details1, col_details2 = st.columns(2)
                
                with col_details1:
                    st.markdown("#### Flight Details")
                    st.markdown(f"**Departure:** {flight.get('departure_time', '')} on {flight.get('departure_date', '')}")
                    st.markdown(f"**Arrival:** {flight.get('arrival_time', '')}")
                    st.markdown(f"**Duration:** {flight.get('duration', '')}")
                    st.markdown(f"**Class:** {flight.get('class', 'Economy')}")
                    st.markdown(f"**Aircraft:** {flight.get('aircraft', 'N/A')}")
                
                with col_details2:
                    st.markdown("#### Passenger Details")
                    passengers = booking.get('passenger_details', {}).get('passengers', [])
                    for i, passenger in enumerate(passengers, 1):
                        st.markdown(f"**Passenger {i}:** {passenger.get('first_name', '')} {passenger.get('last_name', '')}")
                
                # Actions
                st.markdown("---")
                col_actions1, col_actions2, col_actions3 = st.columns(3)
                with col_actions1:
                    if st.button("📄 Download Ticket", key=f"ticket_{booking.get('booking_id')}", use_container_width=True):
                        st.success("Ticket downloaded! (Mock feature)")
                with col_actions2:
                    if st.button("🔄 Modify Booking", key=f"modify_{booking.get('booking_id')}", use_container_width=True):
                        st.info("Modification feature coming soon!")
                with col_actions3:
                    if st.button("🗑️ Cancel Booking", key=f"cancel_{booking.get('booking_id')}", use_container_width=True):
                        st.warning("Cancellation feature coming soon!")
    
    # Back button
    if st.button("← Back to Flight Search"):
        st.session_state.flight_booking_step = "search"
        st.rerun()

def integrate_flights_with_itinerary(destination: str, start_date: str, budget: float):
    """Get flight suggestions for an itinerary"""
    flight_booker = FlightBooking()
    
    # Map destinations to airport codes
    destination_mapping = {
        "Dubai": "DXB",
        "Bangkok": "BKK",
        "Thailand": "BKK",
        "Singapore": "SIN",
        "Paris": "CDG",
        "France": "CDG",
        "London": "LHR",
        "UK": "LHR",
        "New York": "JFK",
        "USA": "JFK",
        "Maldives": "MLE",
        "Bali": "DPS",
        "Indonesia": "DPS",
        "Goa": "GOI",
        "Mumbai": "BOM",
        "Delhi": "DEL",
        "Bangalore": "BLR",
        "Chennai": "MAA",
        "Kolkata": "CCU",
        "Hyderabad": "HYD"
    }
    
    # Get airport code for destination
    dest_code = destination_mapping.get(destination, "DEL")  # Default to Delhi if not found
    
    # Suggest flights from major Indian cities
    suggestions = []
    for from_city in ["Delhi (DEL)", "Mumbai (BOM)", "Bangalore (BLR)", "Chennai (MAA)"]:
        flights = flight_booker.search_flights(
            from_city=from_city,
            to_city=dest_code,
            departure_date=start_date,
            passengers=1,
            flight_class="Economy"
        )
        
        if flights:
            # Get the cheapest flight
            cheapest = min(flights, key=lambda x: x["price"])
            suggestions.append({
                "from": from_city,
                "flight": cheapest,
                "within_budget": cheapest["price"] <= budget
            })
    
    return suggestions

# Test function
def test_flight_module():
    """Test the flight booking module"""
    st.title("✈️ Flight Module Test")
    
    # Create test user if not logged in
    if 'test_user' not in st.session_state:
        st.session_state.test_user = {"email": "test@example.com", "name": "Test User"}
        st.session_state.authenticated = True
        st.session_state.current_user = st.session_state.test_user
    
    show_flight_booking_page()

if __name__ == "__main__":
    test_flight_module()