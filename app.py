import streamlit as st
from utils.audio_fixer import fix_audio_issues
import os

st.set_page_config(page_title="TrackCheck Audio Fixer", layout="centered")

st.title("🎧 TrackCheck – Audio Fixer Tool")

st.markdown(
    """
    Upload a WAV audio file and automatically fix clipping, normalize loudness, 
    apply fade-out, and export a clean version ready for Offstep QC.  
    """
)

uploaded_file = st.file_uploader("📂 Upload your WAV file", type=["wav"])

if uploaded_file is not None:
    with st.spinner("Analyzing and fixing your track..."):
        input_path = os.path.join("temp_input.wav")
        output_path = os.path.join("fixed_audio.wav")

        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        result_path, message = fix_audio_issues(input_path, output_path)
        st.success(message)

        audio_file = open(result_path, "rb")
        st.download_button("⬇️ Download Fixed Audio", audio_file, file_name="fixed_audio.wav")