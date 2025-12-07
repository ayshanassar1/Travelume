import streamlit as st

def render_categories():
    """Render category filter section"""
    categories = [
        {"icon": "🏖️", "name": "Beach", "count": "240+ destinations"},
        {"icon": "🏔️", "name": "Mountains", "count": "180+ destinations"},
        {"icon": "🏙️", "name": "City Breaks", "count": "320+ destinations"},
        {"icon": "🏕️", "name": "Adventure", "count": "150+ destinations"},
        {"icon": "🏛️", "name": "Cultural", "count": "210+ destinations"},
        {"icon": "🍜", "name": "Foodie", "count": "190+ destinations"},
        {"icon": "💝", "name": "Romantic", "count": "120+ destinations"},
        {"icon": "👨‍👩‍👧‍👦", "name": "Family", "count": "170+ destinations"},
    ]
    
    st.markdown("""
    <style>
    .categories-section {
        padding: 60px 20px;
        background: #f8f9fa;
        border-radius: 30px;
        margin: 40px 0;
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .section-subtitle {
        color: #666;
        text-align: center;
        margin-bottom: 40px;
        font-size: 1.1rem;
    }
    
    .categories-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .category-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .category-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .category-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    
    .category-count {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
    
    <div class="categories-section">
        <h2 class="section-title">Explore by Category</h2>
        <p class="section-subtitle">Find your perfect trip based on your interests</p>
        
        <div class="categories-grid">
    """, unsafe_allow_html=True)
    
    # Create grid
    cols = st.columns(4)
    for idx, cat in enumerate(categories):
        with cols[idx % 4]:
            html = f"""
            <div class="category-card" onclick="window.location.href='?page=category&cat={cat['name'].lower()}'">
                <div class="category-icon">{cat['icon']}</div>
                <div class="category-name">{cat['name']}</div>
                <div class="category-count">{cat['count']}</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)