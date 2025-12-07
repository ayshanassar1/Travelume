import streamlit as st
import google.generativeai as genai

# Force black text
st.markdown("<style>*{color:black !important; background:white !important;}</style>", unsafe_allow_html=True)

st.title("🧪 Simple AI Test")

# Get API key
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Use the working model from your test
model = genai.GenerativeModel('models/gemini-pro-latest')

# Simple form
destination = st.text_input("Where to?", "Dubai")
days = st.slider("Days", 1, 10, 3)

if st.button("Generate Simple Itinerary"):
    with st.spinner("Generating..."):
        try:
            prompt = f"Create a {days}-day itinerary for {destination}. Include activities and costs."
            response = model.generate_content(prompt)
            
            # Display result
            st.success("✅ Itinerary Generated!")
            st.divider()
            st.markdown(f"## {destination} Itinerary ({days} days)")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")