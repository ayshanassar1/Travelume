import streamlit as st

def render_hero():
    """Render Rutugo-style hero section with search"""
    st.markdown("""
    <style>
    .hero-container {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        height: 70vh;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white;
        padding: 0 20px;
        border-radius: 0 0 30px 30px;
        margin-bottom: 40px;
    }
    
    .hero-content {
        max-width: 800px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin-bottom: 40px;
        opacity: 0.9;
    }
    
    .search-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        max-width: 800px;
        margin: 0 auto;
    }
    
    .search-tabs {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .search-tab {
        padding: 10px 25px;
        border-radius: 25px;
        background: #f8f9fa;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .search-tab.active {
        background: #2E65F3;
        color: white;
    }
    
    .search-inputs {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }
    
    .search-input {
        padding: 12px 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        font-size: 16px;
        width: 100%;
    }
    
    .search-button {
        background: #2E65F3;
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s;
    }
    
    .search-button:hover {
        background: #1e4fcf;
        transform: translateY(-2px);
    }
    
    @media (max-width: 768px) {
        .hero-container { height: 60vh; }
        .hero-title { font-size: 2.5rem; }
        .search-inputs { grid-template-columns: 1fr; }
    }
    </style>
    
    <div class="hero-container">
        <div class="hero-content">
            <h1 class="hero-title">Discover Your Next Adventure</h1>
            <p class="hero-subtitle">AI-powered travel planning for every type of traveler</p>
            
            <div class="search-box">
                <div class="search-tabs">
                    <div class="search-tab active">Destinations</div>
                    <div class="search-tab">Itineraries</div>
                    <div class="search-tab">Experiences</div>
                    <div class="search-tab">Hotels</div>
                </div>
                
                <div class="search-inputs">
                    <input type="text" class="search-input" placeholder="Where do you want to go?" id="destination-input">
                    <input type="text" class="search-input" placeholder="Check-in" onfocus="(this.type='date')" onblur="(this.type='text')">
                    <input type="text" class="search-input" placeholder="Check-out" onfocus="(this.type='date')" onblur="(this.type='text')">
                    <select class="search-input">
                        <option>Travelers</option>
                        <option>1 Traveler</option>
                        <option>2 Travelers</option>
                        <option>3+ Travelers</option>
                    </select>
                </div>
                
                <button class="search-button" onclick="startSearch()">
                    <i class="fas fa-search"></i> Explore Destinations
                </button>
            </div>
        </div>
    </div>
    
    <script>
    function startSearch() {
        const destination = document.getElementById('destination-input').value;
        if(destination) {
            window.location.href = window.location.origin + '?page=search&q=' + encodeURIComponent(destination);
        }
    }
    
    // Make tabs clickable
    document.querySelectorAll('.search-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    </script>
    """, unsafe_allow_html=True)