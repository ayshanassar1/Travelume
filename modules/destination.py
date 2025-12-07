import streamlit as st

def render_destination_grid():
    """Render destination cards grid like Rutugo"""
    destinations = [
        {
            "id": "dubai",
            "name": "Dubai",
            "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "description": "Luxury desert metropolis with skyscrapers, shopping & desert adventures",
            "rating": 4.8,
            "reviews": 1243,
            "price": "₹60K+",
            "days": "5-7 days",
            "tags": ["Luxury", "Desert", "Modern", "Shopping"]
        },
        {
            "id": "thailand",
            "name": "Thailand",
            "image": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "description": "Tropical paradise with rich culture, beaches, and delicious cuisine",
            "rating": 4.9,
            "reviews": 2187,
            "price": "₹40K+",
            "days": "7-10 days",
            "tags": ["Beaches", "Culture", "Food", "Islands"]
        },
        {
            "id": "bali",
            "name": "Bali",
            "image": "https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "description": "Island of gods with temples, rice terraces & spiritual retreats",
            "rating": 4.7,
            "reviews": 1890,
            "price": "₹45K+",
            "days": "6-8 days",
            "tags": ["Beaches", "Spiritual", "Nature", "Wellness"]
        },
        {
            "id": "paris",
            "name": "Paris",
            "image": "https://images.unsplash.com/photo-1502602898536-47ad22581b52?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "description": "City of love with iconic landmarks, art, and exquisite cuisine",
            "rating": 4.6,
            "reviews": 3120,
            "price": "₹80K+",
            "days": "4-6 days",
            "tags": ["Romantic", "Art", "Food", "History"]
        },
        {
            "id": "maldives",
            "name": "Maldives",
            "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "description": "Overwater bungalows & crystal clear waters in tropical paradise",
            "rating": 4.9,
            "reviews": 1560,
            "price": "₹1L+",
            "days": "5-7 days",
            "tags": ["Luxury", "Beaches", "Honeymoon", "Relaxation"]
        },
        {
            "id": "japan",
            "name": "Japan",
            "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80",
            "description": "Ancient temples, modern cities, cherry blossoms & unique culture",
            "rating": 4.8,
            "reviews": 2340,
            "price": "₹70K+",
            "days": "8-12 days",
            "tags": ["Culture", "Food", "Technology", "Nature"]
        }
    ]
    
    st.markdown("""
    <style>
    .destinations-section {
        padding: 60px 20px;
    }
    
    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 40px;
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        margin: 0;
    }
    
    .view-all-link {
        color: #2E65F3;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .destinations-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 30px;
    }
    
    .destination-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .destination-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .card-content {
        padding: 25px;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 15px;
    }
    
    .destination-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #333;
        margin: 0;
    }
    
    .destination-price {
        background: #FF6B6B;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .destination-description {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 15px;
        line-height: 1.5;
    }
    
    .rating {
        display: flex;
        align-items: center;
        gap: 5px;
        margin-bottom: 15px;
    }
    
    .stars {
        color: #FFD700;
    }
    
    .review-count {
        color: #888;
        font-size: 0.9rem;
    }
    
    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 20px;
    }
    
    .tag {
        background: #f0f7ff;
        color: #2E65F3;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }
    
    .duration {
        color: #888;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .view-plan-btn {
        background: transparent;
        color: #2E65F3;
        border: 1px solid #2E65F3;
        padding: 8px 20px;
        border-radius: 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 0.9rem;
    }
    
    .view-plan-btn:hover {
        background: #2E65F3;
        color: white;
    }
    
    @media (max-width: 768px) {
        .destinations-grid { grid-template-columns: 1fr; }
        .section-header { flex-direction: column; align-items: flex-start; gap: 10px; }
    }
    </style>
    
    <div class="destinations-section">
        <div class="section-header">
            <h2 class="section-title">Popular Destinations</h2>
            <a href="?page=all_destinations" class="view-all-link">View All Destinations →</a>
        </div>
    """, unsafe_allow_html=True)
    
    # Create grid using Streamlit columns
    cols = st.columns(3)
    for idx, dest in enumerate(destinations[:6]):
        with cols[idx % 3]:
            render_destination_card(dest)

def render_destination_card(destination):
    """Render a single destination card"""
    html = f"""
    <div class="destination-card" onclick="window.location.href='?page={destination['id']}_plan'">
        <img src="{destination['image']}" alt="{destination['name']}" class="card-image">
        <div class="card-content">
            <div class="card-header">
                <h3 class="destination-name">{destination['name']}</h3>
                <div class="destination-price">{destination['price']}</div>
            </div>
            
            <p class="destination-description">{destination['description']}</p>
            
            <div class="rating">
                <div class="stars">
                    {"★" * int(destination['rating'])}{"☆" * (5 - int(destination['rating']))}
                </div>
                <span class="review-count">({destination['reviews']} reviews)</span>
            </div>
            
            <div class="tags">
                {''.join([f'<span class="tag">{tag}</span>' for tag in destination['tags'][:3]])}
            </div>
            
            <div class="card-footer">
                <div class="duration">
                    <i class="far fa-calendar-alt"></i> {destination['days']}
                </div>
                <button class="view-plan-btn" onclick="window.location.href='?page={destination['id']}_plan'">View Plan</button>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)