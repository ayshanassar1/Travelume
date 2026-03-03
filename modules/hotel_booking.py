"""
Hotel Booking Module for Travelume
Integrates with existing main.py structure
"""

import streamlit as st
import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class HotelBooking:
    """Hotel booking system with real/mock data integration"""
    
    def __init__(self):
        self.hotels_data = self._load_hotels_data()
        self.booking_data = self._load_bookings()
    
    def _load_hotels_data(self) -> Dict:
        """Load hotels data from JSON file or use mock data"""
        hotels_file = "data/hotels.json"
        
        # Create mock data if file doesn't exist
        mock_hotels = {
            "hotels": [
                {
                    "id": "h1",
                    "city": "Paris",
                    "name": "Hôtel Regina Louvre",
                    "address": "2 place des Pyramides, 75001 Paris",
                    "price_per_night": 289,
                    "currency": "EUR",
                    "rating": 4.6,
                    "review_count": 1243,
                    "amenities": ["Free WiFi", "Spa", "Restaurant", "Bar", "Air Conditioning", "Room Service"],
                    "latitude": 48.8647,
                    "longitude": 2.3319,
                    "check_in": "15:00",
                    "check_out": "12:00",
                    "images": [
                        "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800",
                        "https://images.unsplash.com/photo-1566073771259-6a8506099945?w-800"
                    ],
                    "description": "Luxury hotel with stunning views of the Louvre and Eiffel Tower.",
                    "room_types": [
                        {"type": "Standard Room", "price": 289, "max_guests": 2},
                        {"type": "Deluxe Room", "price": 389, "max_guests": 2},
                        {"type": "Suite", "price": 589, "max_guests": 4}
                    ]
                },
                {
                    "id": "h2",
                    "city": "Paris",
                    "name": "Le Bristol Paris",
                    "address": "112 rue du Faubourg Saint-Honoré, 75008 Paris",
                    "price_per_night": 850,
                    "currency": "EUR",
                    "rating": 4.8,
                    "review_count": 892,
                    "amenities": ["Pool", "Spa", "5 Restaurants", "Bar", "Fitness Center", "Butler Service"],
                    "latitude": 48.8725,
                    "longitude": 2.3174,
                    "check_in": "14:00",
                    "check_out": "12:00",
                    "images": [
                        "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800",
                        "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800"
                    ],
                    "description": "Palace hotel with Michelin-starred dining and luxurious accommodations.",
                    "room_types": [
                        {"type": "Deluxe Room", "price": 850, "max_guests": 2},
                        {"type": "Executive Suite", "price": 1200, "max_guests": 2},
                        {"type": "Presidential Suite", "price": 3500, "max_guests": 4}
                    ]
                },
                {
                    "id": "h3",
                    "city": "Dubai",
                    "name": "Burj Al Arab Jumeirah",
                    "address": "Jumeirah Street, Dubai, UAE",
                    "price_per_night": 1500,
                    "currency": "USD",
                    "rating": 4.9,
                    "review_count": 2345,
                    "amenities": ["Private Beach", "Helipad", "Luxury Spa", "9 Restaurants", "Rolls Royce Transfer"],
                    "latitude": 25.1412,
                    "longitude": 55.1852,
                    "check_in": "15:00",
                    "check_out": "12:00",
                    "images": [
                        "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800",
                        "https://images.unsplash.com/photo-1518684079-3c830dcef090?w=800"
                    ],
                    "description": "The world's most luxurious hotel, standing on an artificial island.",
                    "room_types": [
                        {"type": "Deluxe Suite", "price": 1500, "max_guests": 2},
                        {"type": "Panoramic Suite", "price": 2500, "max_guests": 2},
                        {"type": "Royal Suite", "price": 20000, "max_guests": 4}
                    ]
                },
                {
                    "id": "h4",
                    "city": "Dubai",
                    "name": "Atlantis The Palm",
                    "address": "Crescent Road, The Palm Jumeirah, Dubai",
                    "price_per_night": 450,
                    "currency": "USD",
                    "rating": 4.7,
                    "review_count": 5678,
                    "amenities": ["Aquaventure Waterpark", "Aquarium", "Private Beach", "23 Restaurants", "Dolphin Bay"],
                    "latitude": 25.1309,
                    "longitude": 55.1173,
                    "check_in": "15:00",
                    "check_out": "12:00",
                    "images": [
                        "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
                        "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800"
                    ],
                    "description": "Iconic resort with underwater suites and world-class entertainment.",
                    "room_types": [
                        {"type": "Imperial Club Room", "price": 450, "max_guests": 3},
                        {"type": "Underwater Suite", "price": 5000, "max_guests": 2},
                        {"type": "Palm Beach Suite", "price": 1200, "max_guests": 4}
                    ]
                },
                {
                    "id": "h5",
                    "city": "Bali",
                    "name": "Four Seasons Resort Bali at Sayan",
                    "address": "Sayan, Ubud, Bali 80571, Indonesia",
                    "price_per_night": 600,
                    "currency": "USD",
                    "rating": 4.8,
                    "review_count": 987,
                    "amenities": ["Infinity Pool", "Spa", "Yoga Pavilion", "3 Restaurants", "Rice Terrace Views"],
                    "latitude": -8.5069,
                    "longitude": 115.2605,
                    "check_in": "14:00",
                    "check_out": "12:00",
                    "images": [
                        "https://images.unsplash.com/photo-1539367628448-4bc5c9d171c8?w=800",
                        "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=800"
                    ],
                    "description": "Luxury resort nestled in the jungle with breathtaking river valley views.",
                    "room_types": [
                        {"type": "Villa Suite", "price": 600, "max_guests": 2},
                        {"type": "Royal Villa", "price": 1200, "max_guests": 4},
                        {"type": "Presidential Villa", "price": 2500, "max_guests": 6}
                    ]
                },
                {
                    "id": "h6",
                    "city": "Thailand",
                    "name": "Banyan Tree Phuket",
                    "address": "33 Moo 4, Srisoonthorn Road, Phuket 83110, Thailand",
                    "price_per_night": 350,
                    "currency": "USD",
                    "rating": 4.7,
                    "review_count": 1456,
                    "amenities": ["Private Pool Villas", "Spa", "Golf Course", "4 Restaurants", "Beach Access"],
                    "latitude": 7.9500,
                    "longitude": 98.3333,
                    "check_in": "14:00",
                    "check_out": "12:00",
                    "images": [
                        "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800",
                        "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800"
                    ],
                    "description": "All-pool villa resort with panoramic views of the Andaman Sea.",
                    "room_types": [
                        {"type": "Pool Villa", "price": 350, "max_guests": 2},
                        {"type": "Double Pool Villa", "price": 550, "max_guests": 4},
                        {"type": "Ocean View Pool Villa", "price": 650, "max_guests": 2}
                    ]
                }
            ]
        }
        
        try:
            if os.path.exists(hotels_file):
                with open(hotels_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "hotels" in data:
                        return data
            # Create file with mock data
            os.makedirs(os.path.dirname(hotels_file), exist_ok=True)
            with open(hotels_file, 'w', encoding='utf-8') as f:
                json.dump(mock_hotels, f, indent=2)
            return mock_hotels
        except Exception as e:
            st.error(f"Error loading hotels data: {e}")
            return mock_hotels
    
    def _load_bookings(self) -> Dict:
        """Load existing bookings"""
        bookings_file = "data/hotel_bookings.json"
        try:
            if os.path.exists(bookings_file):
                with open(bookings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {"bookings": []}
    
    def _save_bookings(self):
        """Save bookings to file"""
        bookings_file = "data/hotel_bookings.json"
        os.makedirs(os.path.dirname(bookings_file), exist_ok=True)
        with open(bookings_file, 'w', encoding='utf-8') as f:
            json.dump(self.booking_data, f, indent=2)
    
    def search_hotels(self, city: str, check_in: str, check_out: str, 
                     guests: int = 2, min_price: int = 0, 
                     max_price: int = 10000, min_rating: float = 0) -> List[Dict]:
        """Search hotels by criteria"""
        results = []
        for hotel in self.hotels_data.get("hotels", []):
            if hotel["city"].lower() == city.lower():
                # Check price range
                if min_price <= hotel["price_per_night"] <= max_price:
                    # Check rating
                    if hotel["rating"] >= min_rating:
                        # Check room availability for guests
                        for room in hotel.get("room_types", []):
                            if room["max_guests"] >= guests:
                                results.append(hotel)
                                break
        return results
    
    def book_hotel(self, hotel_id: str, user_email: str, room_type: str,
                  check_in: str, check_out: str, guests: int,
                  special_requests: str = "") -> Optional[Dict]:
        """Book a hotel room"""
        # Find hotel
        hotel = None
        for h in self.hotels_data.get("hotels", []):
            if h["id"] == hotel_id:
                hotel = h
                break
        
        if not hotel:
            return None
        
        # Calculate stay duration and total price
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days
        
        # Find room price
        room_price = hotel["price_per_night"]
        for room in hotel.get("room_types", []):
            if room["type"] == room_type:
                room_price = room["price"]
                break
        
        total_price = room_price * nights
        
        # Create booking
        booking_id = f"booking_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        booking = {
            "id": booking_id,
            "hotel_id": hotel_id,
            "hotel_name": hotel["name"],
            "user_email": user_email,
            "room_type": room_type,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "guests": guests,
            "room_price": room_price,
            "total_price": total_price,
            "currency": hotel.get("currency", "USD"),
            "status": "confirmed",
            "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "special_requests": special_requests
        }
        
        # Save booking
        self.booking_data["bookings"].append(booking)
        self._save_bookings()
        
        return booking
    
    def get_user_bookings(self, user_email: str) -> List[Dict]:
        """Get all bookings for a user"""
        user_bookings = []
        for booking in self.booking_data.get("bookings", []):
            if booking["user_email"] == user_email:
                user_bookings.append(booking)
        return user_bookings
    
    def cancel_booking(self, booking_id: str, user_email: str) -> bool:
        """Cancel a booking"""
        for i, booking in enumerate(self.booking_data.get("bookings", [])):
            if booking["id"] == booking_id and booking["user_email"] == user_email:
                # Update status
                self.booking_data["bookings"][i]["status"] = "cancelled"
                self.booking_data["bookings"][i]["cancelled_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_bookings()
                return True
        return False

# Streamlit UI Components
def show_hotel_search():
    """Display hotel search interface"""
    st.markdown("### 🏨 Find & Book Hotels")
    
    # Search form
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            city = st.text_input("City", value="Paris", placeholder="Enter city name")
        with col2:
            check_in = st.date_input("Check-in", value=datetime.now() + timedelta(days=7))
        with col3:
            check_out = st.date_input("Check-out", value=datetime.now() + timedelta(days=10))
        with col4:
            guests = st.number_input("Guests", min_value=1, max_value=10, value=2)
        
        col5, col6, col7 = st.columns(3)
        with col5:
            min_price = st.number_input("Min Price", min_value=0, max_value=10000, value=0)
        with col6:
            max_price = st.number_input("Max Price", min_value=0, max_value=10000, value=1000)
        with col7:
            min_rating = st.slider("Min Rating", min_value=0.0, max_value=5.0, value=4.0, step=0.5)
        
        if st.button("🔍 Search Hotels", type="primary", use_container_width=True):
            return {
                "city": city,
                "check_in": check_in.strftime("%Y-%m-%d"),
                "check_out": check_out.strftime("%Y-%m-%d"),
                "guests": guests,
                "min_price": min_price,
                "max_price": max_price,
                "min_rating": min_rating
            }
    
    return None

def display_hotel_card(hotel: Dict, show_book_button: bool = True):
    """Display a hotel card in UI"""
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Hotel image
            if hotel.get("images"):
                st.image(hotel["images"][0], use_column_width=True)
            else:
                st.image("🏨", width=150)
        
        with col2:
            # Hotel info
            st.markdown(f"#### {hotel['name']}")
            st.markdown(f"📍 {hotel['address']}")
            
            # Rating
            rating_stars = "⭐" * int(hotel["rating"])
            st.markdown(f"{rating_stars} {hotel['rating']} ({hotel.get('review_count', 0)} reviews)")
            
            # Price
            st.markdown(f"### {hotel['currency']} {hotel['price_per_night']} / night")
            
            # Amenities
            amenities_text = ", ".join(hotel.get("amenities", [])[:3])
            st.markdown(f"**Amenities:** {amenities_text}")
            
            # Room types
            if hotel.get("room_types"):
                room_options = [room["type"] for room in hotel["room_types"]]
                selected_room = st.selectbox("Select Room Type", room_options, 
                                           key=f"room_{hotel['id']}")
            
            # Book button
            if show_book_button and st.session_state.get("authenticated"):
                if st.button("📅 Book Now", key=f"book_{hotel['id']}", use_container_width=True):
                    return hotel
            elif not st.session_state.get("authenticated"):
                st.info("Login to book this hotel")
    
    return None

def show_booking_form(hotel: Dict):
    """Display booking form for a hotel"""
    st.markdown(f"### 📝 Book {hotel['name']}")
    
    with st.form(key=f"booking_form_{hotel['id']}"):
        # User info
        col1, col2 = st.columns(2)
        with col1:
            guest_name = st.text_input("Full Name", 
                                      value=st.session_state.get("current_user", {}).get("name", ""))
        with col2:
            guest_email = st.text_input("Email",
                                       value=st.session_state.get("current_user", {}).get("email", ""))
        
        # Room selection
        room_types = hotel.get("room_types", [])
        room_options = [f"{room['type']} - {hotel['currency']} {room['price']}/night" 
                       for room in room_types]
        selected_room = st.selectbox("Room Type", room_options)
        
        # Extract room type from selection
        room_type = selected_room.split(" - ")[0]
        
        # Dates
        col3, col4 = st.columns(2)
        with col3:
            check_in = st.date_input("Check-in", value=datetime.now() + timedelta(days=7))
        with col4:
            check_out = st.date_input("Check-out", value=datetime.now() + timedelta(days=10))
        
        # Guests
        guests = st.number_input("Number of Guests", min_value=1, max_value=10, value=2)
        
        # Special requests
        special_requests = st.text_area("Special Requests", 
                                       placeholder="Early check-in, dietary restrictions, etc.")
        
        # Calculate price
        nights = (check_out - check_in).days
        room_price = next((room["price"] for room in room_types if room["type"] == room_type), 
                         hotel["price_per_night"])
        total_price = room_price * nights
        
        st.markdown(f"### 💰 Total: {hotel['currency']} {total_price} for {nights} nights")
        
        # Terms
        st.checkbox("I agree to the hotel's cancellation policy and terms", key=f"terms_{hotel['id']}")
        
        # Submit button
        submitted = st.form_submit_button("Confirm Booking", type="primary")
        
        if submitted:
            if guest_name and guest_email:
                # Create booking
                hotel_booking = HotelBooking()
                booking = hotel_booking.book_hotel(
                    hotel_id=hotel["id"],
                    user_email=guest_email,
                    room_type=room_type,
                    check_in=check_in.strftime("%Y-%m-%d"),
                    check_out=check_out.strftime("%Y-%m-%d"),
                    guests=guests,
                    special_requests=special_requests
                )
                
                if booking:
                    st.success(f"✅ Booking confirmed! Your booking ID: {booking['id']}")
                    st.balloons()
                    return booking
                else:
                    st.error("Booking failed. Please try again.")
            else:
                st.error("Please fill in all required fields.")
    
    return None

def show_user_bookings():
    """Display user's hotel bookings"""
    if not st.session_state.get("authenticated"):
        st.warning("Please login to view your bookings")
        return
    
    user_email = st.session_state.current_user["email"]
    hotel_booking = HotelBooking()
    bookings = hotel_booking.get_user_bookings(user_email)
    
    if not bookings:
        st.info("📭 You don't have any hotel bookings yet.")
        return
    
    st.markdown("### 📋 My Hotel Bookings")
    
    for booking in bookings:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"#### {booking['hotel_name']}")
                st.markdown(f"**Booking ID:** {booking['id']}")
                st.markdown(f"**Room Type:** {booking['room_type']}")
                st.markdown(f"**Check-in:** {booking['check_in']} | **Check-out:** {booking['check_out']}")
                st.markdown(f"**Guests:** {booking['guests']} | **Nights:** {booking['nights']}")
            
            with col2:
                st.markdown("##### Price Details")
                st.markdown(f"**Nightly:** {booking['currency']} {booking['room_price']}")
                st.markdown(f"**Total:** {booking['currency']} {booking['total_price']}")
                st.markdown(f"**Status:** {booking['status'].upper()}")
                st.markdown(f"**Booked on:** {booking['booking_date']}")
            
            with col3:
                if booking["status"] == "confirmed":
                    if st.button("Cancel", key=f"cancel_{booking['id']}", type="secondary"):
                        if hotel_booking.cancel_booking(booking["id"], user_email):
                            st.success("Booking cancelled successfully!")
                            st.rerun()

# Main hotel booking page
def show_hotel_booking_page():
    """Main hotel booking page"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
        <h1 style="color: black !important; font-weight: 900; font-size: 2.5rem;">🏨 Hotel Booking</h1>
        <p style="color: #7f8c8d !important; font-size: 1.2rem;">Find and book hotels worldwide</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2 = st.tabs(["🔍 Search Hotels", "📋 My Bookings"])
    
    with tab1:
        # Search interface
        search_params = show_hotel_search()
        
        if search_params:
            hotel_booking = HotelBooking()
            hotels = hotel_booking.search_hotels(**search_params)
            
            if hotels:
                st.markdown(f"### Found {len(hotels)} hotels in {search_params['city']}")
                
                # Display hotels
                selected_hotel = None
                for hotel in hotels:
                    hotel_selected = display_hotel_card(hotel)
                    if hotel_selected:
                        selected_hotel = hotel_selected
                        break
                
                # Show booking form if hotel selected
                if selected_hotel:
                    show_booking_form(selected_hotel)
            else:
                st.warning(f"No hotels found in {search_params['city']} matching your criteria.")
    
    with tab2:
        show_user_bookings()
    
    # Back button
    st.markdown("---")
    if st.button("← Back to Home", key="back_from_hotels"):
        st.session_state.current_page = 'home'
        st.rerun()

# Integration with AI Planner
def integrate_hotels_with_itinerary(destination: str, check_in: str, check_out: str, 
                                   guests: int = 2, budget: float = None):
    """
    Get hotel recommendations for an AI-generated itinerary
    This can be called from ai_planner.py
    """
    hotel_booking = HotelBooking()
    
    # Default search parameters
    search_params = {
        "city": destination,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests
    }
    
    # Adjust price range based on budget
    if budget:
        # Assume 30% of total budget for accommodation
        accommodation_budget = budget * 0.3
        nights = (datetime.strptime(check_out, "%Y-%m-%d") - 
                 datetime.strptime(check_in, "%Y-%m-%d")).days
        if nights > 0:
            nightly_budget = accommodation_budget / nights
            search_params["min_price"] = int(nightly_budget * 0.5)
            search_params["max_price"] = int(nightly_budget * 1.5)
    
    hotels = hotel_booking.search_hotels(**search_params)
    
    # Return top 3 hotels within budget
    return hotels[:3]

# Test function
if __name__ == "__main__":
    # Test the hotel booking system
    hotel_booking = HotelBooking()
    print(f"Loaded {len(hotel_booking.hotels_data.get('hotels', []))} hotels")
    
    # Search test
    hotels = hotel_booking.search_hotels("Paris", "2024-12-25", "2024-12-30")
    print(f"Found {len(hotels)} hotels in Paris")