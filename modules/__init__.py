"""
Travelume Modules Package
Backend modules for AI travel planning

This file makes the modules folder a Python package.
"""

__version__ = "1.0.0"
__author__ = "Travelume Team"
__description__ = "AI-Powered Travel Planning Platform"

# Export main classes and functions
from .database import Database, get_database
from .ai_planner import render_ai_planner

# List of all available modules
__all__ = [
    # Database
    'Database',
    'get_database',
    
    # AI Planner
    'render_ai_planner',
    
    # Future modules (commented out for now)
    # 'WeatherAPI',
    # 'CurrencyAPI',
    # 'MapsModule',
    # 'ExportModule',
]

# Package metadata
__metadata__ = {
    "name": "travelume_modules",
    "version": __version__,
    "author": __author__,
    "description": __description__,
    "modules_available": [
        "database",
        "ai_planner"
    ]
}

def get_module_info():
    """Get information about available modules"""
    return __metadata__

def check_dependencies():
    """Check if required dependencies are available"""
    import sys
    import importlib
    
    required_packages = [
        "streamlit",
        "google-generativeai",
        "python-dotenv",
        "requests"
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️ Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    return True

# Initialize on import
print(f"[OK] Travelume Modules v{__version__} loaded successfully!")