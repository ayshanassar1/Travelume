"""
Test Backend Integration for Travelume
"""

import sys
import os

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🧪 Testing Travelume Backend Integration...")
print("=" * 50)

# Test 1: Check if modules can be imported
print("\n1. Testing module imports...")
try:
    from modules.database import get_database
    print("✅ Database module imported successfully")
    
    from modules.ai_planner import render_ai_planner
    print("✅ AI Planner module imported successfully")
    
    from modules import __version__
    print(f"✅ Package version: {__version__}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you have created all module files:")
    print("   - modules/__init__.py")
    print("   - modules/database.py")
    print("   - modules/ai_planner.py")

# Test 2: Check dependencies
print("\n2. Checking dependencies...")
required_packages = [
    "streamlit",
    "google.generativeai",
    "requests",
    "python-dotenv"
]

missing = []
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
        print(f"✅ {package}")
    except ImportError:
        missing.append(package)
        print(f"❌ {package} (missing)")

if missing:
    print(f"\n⚠️ Missing packages: {', '.join(missing)}")
    print("Install with: pip install " + " ".join(missing))
else:
    print("\n✅ All dependencies installed!")

# Test 3: Test database initialization
print("\n3. Testing database initialization...")
try:
    db = get_database()
    print("✅ Database initialized successfully")
    
    # Check data directory
    if os.path.exists("data"):
        print("✅ Data directory exists")
        files = os.listdir("data")
        print(f"   Files in data/: {files}")
    else:
        print("⚠️ Data directory not created yet (will be created on first run)")
        
except Exception as e:
    print(f"❌ Database initialization failed: {e}")

print("\n" + "=" * 50)
print("🎯 Backend Test Complete!")

if len(missing) == 0:
    print("✅ Ready to run: streamlit run main.py")
else:
    print("⚠️ Install missing packages first")