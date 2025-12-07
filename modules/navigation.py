"""
Navigation Module for Travelume
Provides a modern navigation bar similar to Rutugo.com
"""

import streamlit as st

def create_navigation():
    """
    Creates a modern navigation bar with logo and menu items
    """
    
    # Custom CSS for navigation styling
    st.markdown("""
    <style>
    /* Navigation bar styling */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .nav-logo {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1e88e5;
        text-decoration: none;
    }
    
    .nav-logo span {
        color: #ff6b6b;
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .nav-item a {
        text-decoration: none;
        color: #333;
        font-weight: 500;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .nav-item a:hover {
        background-color: #f0f8ff;
        color: #1e88e5;
    }
    
    .nav-actions {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .login-btn {
        background-color: transparent;
        color: #1e88e5;
        border: 1px solid #1e88e5;
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 500;
    }
    
    .signup-btn {
        background-color: #1e88e5;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 500;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .navbar {
            flex-direction: column;
            padding: 1rem;
        }
        
        .nav-menu {
            flex-wrap: wrap;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .nav-actions {
            margin-top: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation bar HTML
    st.markdown("""
    <div class="navbar">
        <div class="nav-logo">
            Travel<span>ume</span>
        </div>
        
        <ul class="nav-menu">
            <li class="nav-item"><a href="#home">Home</a></li>
            <li class="nav-item"><a href="#destinations">Destinations</a></li>
            <li class="nav-item"><a href="#itineraries">Itineraries</a></li>
            <li class="nav-item"><a href="#ai-planner">AI Planner</a></li>
            <li class="nav-item"><a href="#community">Community</a></li>
            <li class="nav-item"><a href="#about">About</a></li>
        </ul>
        
        <div class="nav-actions">
            <button class="login-btn" onclick="alert('Login feature coming soon!')">Log In</button>
            <button class="signup-btn" onclick="alert('Sign up feature coming soon!')">Sign Up</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_navigation():
    """
    Main function to display navigation
    """
    create_navigation()

if __name__ == "__main__":
    show_navigation()