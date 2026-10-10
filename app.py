import streamlit as st
import urllib.parse
import requests

# Page Setup
st.set_page_config(page_title="Zeno AI Studio", page_icon="⚡", layout="wide")

# Header
st.title("⚡ Zeno AI Studio")
st.caption("Your free all-in-one AI assistant for chat, photo generation, and video scenes.")

# Sidebar Controls
st.sidebar.title("⚙️ Zeno Settings")
app_mode = st.sidebar.radio("Select Mode:", ["🤖 Chat & Info Assistant", "🎨 Real Photo Generator", "🎬 Video Generator"])

# ==========================================
# MODE 1: CHAT & INFORMATION ASSISTANT
# ==========================================
if app_mode == "🤖 Chat & Info Assistant":
    st.subheader("💬 Chat with Zeno")
    st.write("Ask Zeno anything—from coding help and homework questions to general knowledge!")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am Zeno. How can I help you today?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Zeno something..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Zeno is thinking..."):
                try:
                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                    headers = {"User-Agent": "Mozilla/5.0"}
                    res = requests.get(url, headers=headers, timeout=15)
                    
                    if res.status_code == 200 and res.text.strip():
                        response_text = res.text
                    else:
                        response_text = f"I am Zeno! Regarding **'{prompt}'**, feel free to ask me anything."
                except Exception:
                    response_text = f"I am ready to help you with **'{prompt}'**!"

                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

# ==========================================
# MODE 2: REAL PHOTO GENERATOR
# ==========================================
elif app_mode == "🎨 Real Photo Generator":
    st.subheader("🎨 Zeno Automotive & Real Photo Generator")
    st.write("Generate high-quality realistic photographs and download them directly inside Zeno.")
    
    st.info("💡 **Realism Tip:** Describe the specific model, environment, and natural lighting.")

    img_prompt = st.text_input(
        "Describe the photo scene:", 
        "A black stock BMW M4 Competition parked on wet asphalt in an urban parking lot, natural overcast lighting, detailed paint reflections, realistic tire texture, DSLR photo"
    )

    if st.button("Generate Real Photo"):
        if not img_prompt.strip():
            st.warning("Please type a description first!")
        else:
            with st.spinner("Zeno is capturing the photograph... 📸"):
                camera_tags = "RAW photograph, natural lighting, candid shot, detailed asphalt texture, depth of field, subtle film grain, unedited camera output"
                full_prompt = f"{img_prompt}, {camera_tags}"
                encoded_img = urllib.parse.quote(full_prompt)
                
                img_url = f"https://image.pollinations.ai/prompt/{encoded_img}?width=1280&height=720&model=flux-realism&nologo=true&seed=42"
                
                try:
                    img_data = requests.get(img_url, timeout=30).content
                    
                    st.image(img_data, caption=f"Zeno Photography: '{img_prompt}'", use_container_width=True)
                    st.success("Photo generated successfully! 🎉")
                    
                    st.download_button(
                        label="💾 Download Real Photo",
                        data=img_data,
                        file_name="zeno_real_photo.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Could not load image directly: {e}")

# ==========================================
# MODE 3: VIDEO GENERATOR
# ==========================================
elif app_mode == "🎬 Video Generator":
    st.subheader("🎬 Zeno Video Generator")
    st.write("Generate video scenes natively inside Zeno.")
    
    vid_prompt = st.text_input("Describe your video scene:", "A stock BMW M4 driving down a real highway at sunset")

    if st.button("Generate Video Scene"):
        if not vid_prompt.strip():
            st.warning("Please type a description first!")
        else:
            with st.spinner("Zeno is assembling video frames... 🎬"):
                encoded_vid = urllib.parse.quote(vid_prompt)
                vid_url = f"https://gen.pollinations.ai/video/{encoded_vid}"
                
                st.video(vid_url)
                st.info("💡 Video servers may queue frames. Re-click 'Generate Video Scene' after 15 seconds if it takes time.")