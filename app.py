import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="Zeno AI Studio", page_icon="⚡", layout="wide")

# Sidebar navigation
st.sidebar.title("⚡ Zeno Settings")
mode = st.sidebar.radio(
    "Select Mode:",
    ["💬 Chat & Info Assistant", "🎨 Real Photo Generator", "🎬 Video Generator"]
)

# Initialize Gemini Client using Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

# --- MODE 1: CHAT ASSISTANT ---
if mode == "💬 Chat & Info Assistant":
    st.title("⚡ Zeno AI Studio")
    st.caption("Your free all-in-one AI assistant for chat, photo generation, and video scenes.")
    
    st.header("💬 Chat with Zeno")
    st.write("Ask Zeno anything—from coding help and homework questions to general knowledge!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am Zeno. How can I help you today?"}
        ]

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if prompt := st.chat_input("Ask Zeno something..."):
        # Store user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate AI response
        with st.chat_message("assistant"):
            if not client:
                error_msg = "⚠️ Gemini API key missing! Please add `GEMINI_API_KEY` to Streamlit Secrets."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                with st.spinner("Zeno is thinking..."):
                    try:
                        # Call Google Gemini API
                        response = client.models.generate_content(
                            model="gemini-1.5-flash",
                            contents=prompt,
                        )
                        answer = response.text
                        st.write(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        err_text = f"An error occurred: {e}"
                        st.error(err_text)
                        st.session_state.messages.append({"role": "assistant", "content": err_text})

# --- MODE 2: PHOTO GENERATOR ---
elif mode == "🎨 Real Photo Generator":
    st.title("🎨 Real Photo Generator")
    st.write("Describe the image you want to generate:")
    img_prompt = st.text_input("Image Prompt:", placeholder="A futuristic BMW racing on Mars...")
    if st.button("Generate Photo"):
        if img_prompt:
            st.info("Photo generation feature active!")
        else:
            st.warning("Please enter a prompt first.")

# --- MODE 3: VIDEO GENERATOR ---
elif mode == "🎬 Video Generator":
    st.title("🎬 Video Generator")
    st.write("Describe the video scene you want to create:")
    vid_prompt = st.text_input("Video Prompt:", placeholder="Cinematic drone shot of a waterfall...")
    if st.button("Generate Video"):
        if vid_prompt:
            st.info("Video generation feature active!")
        else:
            st.warning("Please enter a prompt first.")
