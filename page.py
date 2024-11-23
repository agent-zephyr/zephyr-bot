import streamlit as st
import os
from speech2text import speech2text

def show_page():
    st.title("Video Editor")

    uploaded_file = st.file_uploader("Upload your video", type=['mp4', 'mov', 'avi'])
    
    if uploaded_file is not None:
        os.makedirs("input", exist_ok=True)
        
        with open(os.path.join("input", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Video saved: {uploaded_file.name}")

    preset_options = [
        "Select a preset...",
        "Summarize the main contents of the video",
        "Edit down the video length to two minutes"
    ]
    selected_preset = st.selectbox("Example presets:", preset_options)
    
    if selected_preset != "Select a preset...":
        st.session_state["editing_instructions"] = selected_preset

    editing_instructions = st.text_area(
        "Enter your video editing instructions",
        placeholder="Example: Cut the first 10 seconds, add background music, etc.",
        key="editing_instructions"
    )

    if st.button("Edit My Video"):
        if uploaded_file is not None and editing_instructions:
            st.info("Processing your video...")
            
            # Run transcription on the uploaded video
            video_path = os.path.join("input", uploaded_file.name)
            speech2text.transcribe_video(video_path)
            
            st.video("output/example_output.mp4")
        else:
            st.warning("Please upload a video and provide editing instructions")

    if st.session_state.get('show_output', False):
        st.subheader("Output Video")
        st.video("output/example_output.mp4")

if __name__ == "__main__":
    show_page()
