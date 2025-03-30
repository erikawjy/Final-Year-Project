import os
import json
import streamlit as st

# Set Page Configuration
st.set_page_config(layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: white;'>View video recordings of Intruders</h1>", unsafe_allow_html=True)

recordings_folder_path = "data/recordings"

# Fetch and display recordings
if not os.path.exists(recordings_folder_path) or not os.listdir(recordings_folder_path):
    st.info("No recordings available.")
    
else:
    for folder in sorted(os.listdir(recordings_folder_path), reverse=True):  # Show latest first
        if folder.startswith("."):
            continue

        video_file_path = os.path.join(recordings_folder_path, folder, "motion.mp4")
        json_file_path = os.path.join(recordings_folder_path, folder, "metadata.json")

        # Skip if required files are missing
        if not os.path.exists(json_file_path) or not os.path.exists(video_file_path):
            continue

        # Load metadata
        with open(json_file_path, "r") as f:
            json_data = json.load(f)

        output_video_filename = json_data.get("video_file", "Unknown")
        timestamp = json_data.get("timestamp", "Unknown Time")
        intruder_position = json_data.get("intruder_position", "Unknown Position")
        intruder_type = json_data.get("intruder_type", "Unknown Intruder")

        # Display each recording in a card-style layout
        with st.container():
            st.markdown(
                f"""
                <div class="recording-card">
                    <h3>🚨 {intruder_type.capitalize()} Detected</h3>
                    <p class="metadata">📍 Intruder spotted leaving the <b>{intruder_position}</b> part of the room.</p>
                    <p class="metadata">⏰ Time of occurrence: <b>{timestamp}</b></p>
                    <p class="metadata">📁 Video stored at: <b>{output_video_filename}</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.video(video_file_path, format="video/mp4")