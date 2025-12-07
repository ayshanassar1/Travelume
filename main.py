"""
Travelume - AI Travel Planner
Main Application File
"""

import streamlit as st
import re
import webbrowser
import os
import json
from datetime import datetime

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
    st.session_state.current_page = 'home'  # 'home', 'signup', 'login', 'account', 'community_favorites', 'dubai_plan', 'thailand_plan', 'ai_planner'
if 'users' not in st.session_state:
    # Load users from file if exists, otherwise initialize empty
    try:
        with open('users.json', 'r') as f:
            st.session_state.users = json.load(f)
    except FileNotFoundError:
        st.session_state.users = {}

def save_users():
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(st.session_state.users, f, indent=2)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

# Import AI Planner
try:
    from modules.ai_planner import render_ai_planner
    AI_PLANNER_AVAILABLE = True
except ImportError as e:
    AI_PLANNER_AVAILABLE = False
    st.warning(f"AI Planner module not available: {e}")

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

# Enhanced CSS with better styling
st.markdown("""
<style>
html, body, .main, .block-container, .stApp {
    margin: 0 !important;
    padding: 0 !important;
    background-color: #FFFFFF !important;
}
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
    color: white;
}
.hero-text p {
    font-size: 1.2rem;
    line-height: 1.6;
    margin-bottom: 30px;
    opacity: 0.9;
}
.hero-buttons {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
}
.btn-primary {
    background-color: #FF6B6B;
    color: white;
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
    color: white;
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
    color: #667eea;
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
    color: #000000;
    margin-bottom: 15px;
}
.feature-desc {
    color: #666;
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
    color: #2E65F3;
    margin-bottom: 15px;
    opacity: 0.8;
}
.why-choose-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #000000;
    margin-bottom: 15px;
}
.why-choose-desc {
    color: #555;
    line-height: 1.7;
    font-size: 1.05rem;
}
.community-plans {
    padding: 80px 50px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}
.community-plans-content {
    max-width: 1200px;
    margin: 0 auto;
}
.pricing {
    padding: 80px 50px;
    background-color: #f8f9fa;
}
.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 40px;
    max-width: 1200px;
    margin: 0 auto;
}
.pricing-card {
    background: white;
    padding: 40px 30px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}
.pricing-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}
.pricing-card.popular {
    border-color: #2E65F3;
    transform: scale(1.05);
}
.pricing-card.popular::before {
    content: 'MOST POPULAR';
    position: absolute;
    top: 0;
    right: 0;
    background: #2E65F3;
    color: white;
    padding: 8px 20px;
    font-size: 0.8rem;
    font-weight: 600;
    border-bottom-left-radius: 15px;
}
.pricing-header {
    margin-bottom: 30px;
}
.pricing-name {
    font-size: 1.8rem;
    font-weight: bold;
    color: #000000;
    margin-bottom: 10px;
}
.pricing-price {
    font-size: 3rem;
    font-weight: 900;
    color: #2E65F3;
    margin-bottom: 5px;
}
.pricing-period {
    color: #666;
    font-size: 1rem;
}
.pricing-credits {
    background: #f0f7ff;
    padding: 8px 15px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 20px;
    font-weight: 600;
    color: #2E65F3;
}
.pricing-features {
    text-align: left;
    margin-bottom: 30px;
}
.pricing-feature {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    color: #555;
    font-size: 1rem;
}
.pricing-feature i {
    color: #2E65F3;
    margin-right: 10px;
    font-size: 1.1rem;
}
.pricing-button {
    width: 100%;
    padding: 15px;
    background: #2E65F3;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}
.pricing-button:hover {
    background: #1e4fcf;
    transform: translateY(-2px);
}
.pricing-button.secondary {
    background: transparent;
    color: #2E65F3;
    border: 2px solid #2E65F3;
}
.pricing-button.secondary:hover {
    background: #2E65F3;
    color: white;
}
@media(max-width: 768px){
    .nav { padding: 15px 20px; }
    .hero { padding: 40px 20px; }
    .hero-text h1 { font-size: 2.5rem; }
    .features, .why-choose, .community-plans, .pricing { padding: 40px 20px; }
    .links { margin-right: 15px; }
    .pricing-grid { grid-template-columns: 1fr; }
    .pricing-card.popular { transform: none; }
}
</style>
""", unsafe_allow_html=True)

# Navigation bar with auth buttons in top right
st.markdown("""
<div class="nav">
    <div class="logo" onclick="window.location.href=window.location.origin + '?page=home'">Travelume</div>
    <div class="links">
        <a href="#how-it-works">How it works</a>
        <a href="#why-choose">Why Choose Us</a>
        <a href="#ai-planner-demo" id="aiPlannerLink">AI Planner</a>
        <a href="#community-plans">Community Plans</a>
        <a href="#pricing">Pricing</a>
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

# JavaScript to make AI Planner link work
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Make AI Planner link work
    const aiLink = document.getElementById('aiPlannerLink');
    if (aiLink) {
        aiLink.addEventListener('click', function(e) {
            e.preventDefault();
            // Create a click event for the AI Planner button
            const event = new CustomEvent('ai-planner-click');
            window.dispatchEvent(event);
        });
    }
});

// Listen for the AI Planner click event
window.addEventListener('ai-planner-click', function() {
    // This will be handled by Streamlit
    console.log('AI Planner link clicked');
});
</script>
""", unsafe_allow_html=True)

# Show appropriate page based on current_page
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-text">
                <h1>Your Dream Trip,<br>Your Way</h1>
                <p>
                    Your journey, perfectly planned. Tailored to your style, budget, and time — 
                    so you can focus on exploring, not organizing.
                </p>
                <div class="hero-buttons">
    """, unsafe_allow_html=True)

    # Hero section buttons - Show different buttons based on authentication status
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.authenticated:
            if st.button("Plan Your Trip", key="hero_plan", use_container_width=True):
                st.session_state.current_page = 'account'
                st.rerun()
        else:
            if st.button("Start Planning Free", key="hero_signup", use_container_width=True):
                st.session_state.current_page = 'html_auth'
                st.rerun()
    with col2:
        if st.button("Explore Community Plans", key="hero_community", use_container_width=True):
            st.session_state.current_page = 'community_favorites'
            st.rerun()
    with col3:
        if st.button("🤖 Try AI Planner", key="hero_ai", use_container_width=True):
            if AI_PLANNER_AVAILABLE:
                st.session_state.current_page = 'ai_planner'
                st.rerun()
            else:
                st.error("AI Planner not available yet")

    st.markdown("""
                </div>
                <p style="margin-top: 20px; font-size: 16px; opacity: 0.8;">
                    Join thousands of travelers who plan their perfect trips with Travelume
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
    <div class="features" id="how-it-works">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 2.5rem; color: #333; margin-bottom: 20px;">How It Works</h2>
            <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;">
                Simple steps to create your perfect travel itinerary
            </p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title" style="color: black; font-weight: bold;">Tell Us Your Preferences</h3>
                <p class="feature-desc">Share your travel style, budget, interests, and must-see destinations.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📅</div>
                <h3 class="feature-title" style="color: black; font-weight: bold;">Get Personalized Itinerary</h3>
                <p class="feature-desc">We create a custom travel plan tailored specifically to your needs.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✈️</div>
                <h3 class="feature-title" style="color: black; font-weight: bold;">Travel with Confidence</h3>
                <p class="feature-desc">Enjoy your perfectly planned journey with all details taken care of.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Why Choose Travelume Section
    st.markdown("""
    <div class="why-choose" id="why-choose">
        <div style="text-align: center; margin-bottom: 60px;">
            <h2 style="font-size: 2.5rem; color: #333; margin-bottom: 20px;">Why Choose Travelume</h2>
            <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;">
                Experience the future of travel planning with our intelligent platform
            </p>
        </div>
        <div class="why-choose-grid">
            <div class="why-choose-card">
                <div class="why-choose-number">1</div>
                <h3 class="why-choose-title" style="color: black; font-weight: bold;">AI-Powered Personalized Planning</h3>
                <p class="why-choose-desc">
                    Travelume uses advanced AI and Natural Language Processing to instantly generate smart, 
                    end-to-end itineraries tailored to your preferences, budget, and time.
                </p>
            </div>
            <div class="why-choose-card">
                <div class="why-choose-number">2</div>
                <h3 class="why-choose-title" style="color: black; font-weight: bold;">Smart, Real-World Integration</h3>
                <p class="why-choose-desc">
                    From verified travel agents and live chat assistance to weather-aware updates and 
                    location-based suggestions, Travelume connects digital intelligence with real-world convenience.
                </p>
            </div>
            <div class="why-choose-card">
                <div class="why-choose-number">3</div>
                <h3 class="why-choose-title" style="color: black; font-weight: bold;">Seamless, Safe & Social Travel</h3>
                <p class="why-choose-desc">
                    With features like offline plan access and traveler matching alerts, Travelume ensures 
                    a smooth, secure, and engaging travel experience from start to finish.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI Planner Promo Section (NEW)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 40px; border-radius: 20px; text-align: center; margin: 40px 0;">
        <h2 style="color: white; font-size: 2.5rem; margin-bottom: 20px;">🤖 Try Our AI Trip Planner</h2>
        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 30px;">
            Get a personalized itinerary in seconds with our advanced AI technology
        </p>
        <button onclick="window.location.href=window.location.origin + '?page=ai_planner'" style="background: #FF6B6B; color: white; border: none; padding: 15px 40px; font-size: 1.1rem; border-radius: 10px; cursor: pointer; font-weight: 600;">
            Try AI Planner Now
        </button>
    </div>
    """, unsafe_allow_html=True)

    # Show personalized welcome message if authenticated
    if st.session_state.authenticated:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; text-align: center; margin: 40px 0;">
            <h2 style="color: white; margin-bottom: 15px;">Ready to Plan Your Next Adventure?</h2>
            <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 20px;">
                Start creating your personalized travel itinerary now!
            </p>
            <button style="background: #FF6B6B; color: white; border: none; padding: 12px 30px; font-size: 1.1rem; border-radius: 8px; cursor: pointer;" onclick="window.location.href=window.location.origin + '?page=account'">
                Create My Itinerary
            </button>
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

# Add other page conditions here (account, html_auth, etc.)
# ... (rest of your existing page conditions)

# SIDEBAR - Show for ALL users (logged in or not)
st.sidebar.markdown("## 🧭 Quick Navigation")

# AI Planner button for EVERYONE
if st.sidebar.button("🤖 AI Trip Planner", key="sidebar_ai", use_container_width=True):
    if AI_PLANNER_AVAILABLE:
        st.session_state.current_page = 'ai_planner'
        st.rerun()
    else:
        st.sidebar.error("AI Planner not available")

# Show user info if logged in
if st.session_state.authenticated:
    st.sidebar.success(f"✅ Welcome, {st.session_state.current_user['name']}!")
    if st.sidebar.button("My Account Dashboard", key="sidebar_account", use_container_width=True):
        st.session_state.current_page = 'account'
        st.rerun()
    if st.sidebar.button("Logout", key="sidebar_logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.current_page = 'home'
        st.rerun()
else:
    # Show auth options for non-logged in users
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

# Back to Home button
if st.sidebar.button("🏠 Back to Home", key="sidebar_home", use_container_width=True):
    st.session_state.current_page = 'home'
    st.rerun()