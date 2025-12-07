# Save this as test_api.py in your travelume folder
import streamlit as st
import google.generativeai as genai

st.title("🔧 API Key Test")

# Get your API key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success(f"✅ API key found! First few chars: {api_key[:15]}...")
except:
    st.error("❌ No API key found in secrets.toml")
    st.stop()

# Try to configure
try:
    genai.configure(api_key=api_key)
    st.success("✅ API configured successfully")
except Exception as e:
    st.error(f"❌ Configuration error: {e}")
    st.stop()

# List available models
st.write("### 🔍 Available Models:")
try:
    models = list(genai.list_models())
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            st.write(f"✅ **{model.name}**")
except Exception as e:
    st.error(f"❌ Can't list models: {e}")