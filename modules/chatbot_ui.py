import streamlit as st
import time
from modules.travel_coach import travel_coach

def render_chatbot_sidebar():
    """Renders the AI Travel Coach Chat Interface in the Sidebar"""
    
    # Custom CSS for the chat container in sidebar
    st.markdown("""
    <style>
    /* Chat message container styling */
    .stSidebar .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        margin-bottom: 0.5rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    /* User message specific styling */
    .stSidebar div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f0f7ff !important; /* Light blue for user */
        border-color: #d0e3ff !important;
    }

    /* Assistant message specific styling */
    .stSidebar div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #ffffff !important; /* White for bot */
        border-color: #e0e0e0 !important;
    }

    /* Message content text */
    .stSidebar .stChatMessageContent {
        color: #000000 !important;
        font-family: 'Source Sans Pro', sans-serif !important;
        font-size: 0.95rem !important;
    }
    
    .stSidebar div[data-testid="stChatMessageContent"] p {
        color: #000000 !important;
        line-height: 1.5 !important;
    }
    
    /* Input area styling */
    .stSidebar .stChatInput textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ccc !important;
    }
    
    /* Expander styling to match light theme */
    .stSidebar .streamlit-expanderHeader {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border: 1px solid #e0e0e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display Avatar and Title in Sidebar
    with st.sidebar.expander("🤖 AI Travel Coach", expanded=True):
        # Center the avatar image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center; margin: 0;'>🤖</h1>", unsafe_allow_html=True)
        
        st.markdown("<h4 style='text-align: center; color: black; margin-top: 0;'>Travel Buddy</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #555; font-size: 0.8rem; margin-bottom: 15px;'>Your personal travel planning assistant</p>", unsafe_allow_html=True)
        
        # Initialize session state for chat
        if "chat_session_id" not in st.session_state:
            # Start new session
            user_email = "guest"
            if st.session_state.get("authenticated", False):
                user_email = st.session_state.current_user["email"]
                
            try:
                result = travel_coach.start_session(user_email)
                st.session_state.chat_session_id = result["session_id"]
                st.session_state.chat_history = [
                    {"role": "assistant", "content": result["text"], "audio_url": result.get("audio_url")}
                ]
            except Exception as e:
                st.error(f"Failed to start chat: {e}")
                return

        # Chat container to hold messages
        chat_container = st.container(height=350)
        
        with chat_container:
            # Display chat history
            for message in st.session_state.chat_history:
                avatar_url = "🤖" if message["role"] == "assistant" else "👤"
                with st.chat_message(message["role"], avatar=avatar_url):
                    st.markdown(message["content"])
                    if message.get("audio_url"):
                        st.audio(message["audio_url"], format="audio/mp3", autoplay=False)

        # Chat input within the expander
        if prompt := st.chat_input("Ask me anything...", key="sidebar_chat_input"):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                
                # Get bot response
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Writing..."):
                        try:
                            response = travel_coach.process_message(
                                st.session_state.chat_session_id, 
                                prompt
                            )
                            content = response["text"]
                            st.markdown(content)
                            audio_url = response.get("audio_url")
                            if audio_url:
                                st.audio(audio_url, format='audio/mp3', autoplay=False)
                                st.toast("🔊 Voice message received", icon="🗣️")
                            
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "content": content,
                                "audio_url": audio_url
                            })
                        except Exception as e:
                            st.error(f"Error: {e}")
                            
        # Clear chat button
        if st.button("🔄 New Chat", key="clear_chat_sidebar", use_container_width=True, type="secondary"):
            if "chat_session_id" in st.session_state:
                del st.session_state.chat_session_id
            if "chat_history" in st.session_state:
                del st.session_state.chat_history
            st.rerun()

def render_chatbot_popover():
    """Renders the AI Travel Coach as a Floating Popover"""
    
    # Custom CSS for the floating popover button and chat window
    st.markdown("""
    <style>
    /* POP-OVER BUTTON STYLE */
    div[data-testid="stPopover"] {
        position: fixed;
        /* Position: Top Left */
        top: 15px;
        left: 20px;
        z-index: 1000000;
    }
    
    div[data-testid="stPopover"] > button {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: white !important; /* Force white background */
        border: 2px solid #2E65F3;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        padding: 0;
        overflow: hidden;
        transition: transform 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px; 
    }
    
    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.1);
        border-color: #1a4bd6;
    }

    /* POP-OVER WINDOW BODY STYLE - WHITE THEME */
    div[data-testid="stPopoverBody"] {
        background-color: white !important;
        color: black !important;
        border-radius: 12px;
        border: 1px solid #ddd;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        width: 400px !important;
        max-height: 600px !important;
    }

    /* CHAT MESSAGE STYLING (GLOBAL WITHIN POPOVER) */
    .stChatMessage {
        background-color: white !important;
        border: 1px solid #eee !important;
        border-radius: 10px !important;
        padding: 10px !important;
        margin-bottom: 8px !important;
    }
    
    /* User Message: Light Blue/Gray */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f7f9fc !important;
        border-color: #e3e8f0 !important;
    }
    
    /* Assistant Message: White */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #ffffff !important;
        border-color: #eee !important;
    }

    /* Text Colors */
    .stChatMessageContent, p, div[data-testid="stMarkdownContainer"] p {
        color: #2c3e50 !important;
    }

    /* Chat Input */
    .stChatInput textarea {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # The Popover Trigger
    with st.popover("🤖", use_container_width=False, help="Chat with Travel Buddy"):
        st.markdown("### 🤖 Travel Buddy")
        st.markdown("Your personal AI travel assistant.")
        st.markdown("---")
        
        # Initialize session state for chat if needed
        if "chat_session_id" not in st.session_state:
            user_email = "guest"
            if st.session_state.get("authenticated", False):
                user_email = st.session_state.current_user["email"]
                
            try:
                result = travel_coach.start_session(user_email)
                st.session_state.chat_session_id = result["session_id"]
                
                audio_url = result.get("audio_url")
                if audio_url:
                    st.toast("🔊 Audio message ready", icon="🗣️")

                st.session_state.chat_history = [
                    {
                        "role": "assistant", 
                        "content": result["text"],
                        "audio_url": audio_url
                    }
                ]
            except Exception as e:
                st.error(f"Failed to start chat: {e}")
        
        # Chat History Container
        chat_container = st.container(height=400)
        with chat_container:
            if "chat_history" in st.session_state:
                for message in st.session_state.chat_history:
                    avatar_url = "🤖" if message["role"] == "assistant" else "👤"
                    with st.chat_message(message["role"], avatar=avatar_url):
                        st.markdown(message["content"])
                        if message.get("audio_url"):
                            st.audio(message["audio_url"], format="audio/mp3", autoplay=False)

        # Chat Input
        if prompt := st.chat_input("Ask about destinations, budgets...", key="popover_chat_input"):
            if "chat_history" in st.session_state:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with chat_container:
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(prompt)
                    
                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner("Thinking..."):
                            try:
                                response = travel_coach.process_message(
                                    st.session_state.chat_session_id, 
                                    prompt
                                )
                                content = response["text"]
                                st.markdown(content)
                                
                                audio_url = response.get("audio_url")
                                if audio_url:
                                    st.audio(audio_url, format='audio/mp3', autoplay=False)
                                    st.toast("🔊 New voice message", icon="🗣️")
                                
                                st.session_state.chat_history.append({
                                    "role": "assistant", 
                                    "content": content,
                                    "audio_url": audio_url
                                })
                            except Exception as e:
                                # Session recovery logic
                                if "Invalid Session" in str(e) or "KeyError" in str(e):
                                    try:
                                        user_email = "guest"
                                        if st.session_state.get("authenticated", False):
                                            user_email = st.session_state.current_user["email"]
                                        result = travel_coach.start_session(user_email)
                                        st.session_state.chat_session_id = result["session_id"]
                                        response = travel_coach.process_message(st.session_state.chat_session_id, prompt)
                                        content = response["text"]
                                        st.markdown(content)
                                        audio_url = response.get("audio_url")
                                        if audio_url:
                                            st.audio(audio_url, format='audio/mp3', autoplay=False)
                                        st.session_state.chat_history.append({
                                            "role": "assistant", 
                                            "content": content,
                                            "audio_url": audio_url
                                        })
                                    except Exception as retry_e:
                                        st.error(f"Error recovering chat: {retry_e}")
                                else:
                                    st.error(f"Error: {e}")
                                
        # Clear Chat
        if st.button("Clear Chat", key="clear_popover_chat"):
            if "chat_session_id" in st.session_state:
                del st.session_state.chat_session_id
            if "chat_history" in st.session_state:
                del st.session_state.chat_history
            st.rerun()

def render_chatbot():
    render_chatbot_sidebar()
