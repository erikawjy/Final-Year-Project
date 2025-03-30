import os
import cv2
import json
import imutils
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from email_test import send_email_alert
from utils import preprocess_image, subtract_images

load_dotenv()

#Input the recroding and email variables
recordings_folder_path = "data/recordings"
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
recipient_email = 'xxx@gmail.com'

#Motion detection variables
final_width = 1280
final_height = 720
binary_threshold = 100
min_contour_area_to_trigger_detection = 10000
max_small_object_area = 2000

#Initialise code variables 
run = False
reference_frame = None
movement_detected = False
recording_frames = []  # To store 300 frames for saving
frame_count = 0

#Create recordings folder
os.makedirs(recordings_folder_path, exist_ok=True)  # Making sure that the folder exists

#Configuring the page
st.set_page_config(layout="wide")

#Headers
st.markdown("<h1 style='text-align: center; color: white;'>Live Intruder Detection</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Monitor your room in real-time.</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: white;'>Click 'Start Live Feed' to begin.</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: white;'>Click 'Stop Live Feed' to stop the real-time detection.</h5>", unsafe_allow_html=True)

#Setting up of camera
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

#Setting the buttons on the dashboard
col1, col2 = st.columns([1,1])  
with col1:
    if st.button("Start Live Feed", use_container_width=True, key='start'):
        st.write("Live feed started!")
        run = True
with col2:
    if st.button("Stop Live Feed", use_container_width=True, key='stop'):
        st.write("Live feed stopped!")
        run = False


#Video Streaming Loop
while run:

    #Load frames from camera
    try: 
        #Try reading the camera feed
        status, input_rgb_frame = camera.read()

    except Exception as e:
        print(e)
        print('Unable to show webcam - you need to enable permissions on your machine')
        break

    #Preprocess the input image
    resized_input_rgb_frame, resized_input_gray_frame = preprocess_image(input_rgb_frame, final_width=final_width, final_height=final_height)

    # Initializing the first previous frame 
    if reference_frame is None:
        reference_frame = resized_input_gray_frame
        continue

    #Getting the subtract frames and threshold to make the difference more sinificant 
    abs_diff, thresh_abs_diff = subtract_images(reference_frame, resized_input_gray_frame, binary_threshold=binary_threshold)
    dilated_image = cv2.dilate(thresh_abs_diff, None, iterations=5)

    #Contours
    cnts = cv2.findContours(dilated_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts) # each array is a coordinate with a contour in the image

    
    for c in cnts:            
        if cv2.contourArea(c) > min_contour_area_to_trigger_detection: # only want to take the large contours to avoid noise
            (x, y, w, h) = cv2.boundingRect(c) # generate the bounding box coordinates
            cv2.rectangle(
                img=resized_input_rgb_frame, 
                pt1=(x, y), 
                pt2=(x+w, y+h), 
                color=(0, 0, 255), 
                thickness=3
            ) #Draws a box over the motion detected
            movement_detected = True

            #Determine intruder position
            frame_center = 1280 // 2  #Half of frame width
            if (x + w) // 2 < frame_center:
                intruder_position = "Left"
            else:
                intruder_position = "Right"

    intruder_type = "Small object" if max([cv2.contourArea(c) for c in cnts], default=0) < max_small_object_area else "Big object"

    #Shows frame output
    FRAME_WINDOW.image(resized_input_rgb_frame, channels="BGR")

    #If movement detected, start recording the next 300 frames
    if movement_detected:
        recording_frames.append(resized_input_rgb_frame)
        frame_count += 1

        if frame_count == 300:  # After 300 frames (10 seconds at 30 FPS)

            #Save the video
            video_index = len([f for f in os.listdir(recordings_folder_path) if not f.startswith('.')]) + 1
            output_folder = f"{recordings_folder_path}/motion_{video_index}"
            os.makedirs(output_folder, exist_ok=True)  # Ensure folder exists
            output_video_filename = f"{output_folder}/motion.mp4"
            
            #Define video writer
            fourcc = cv2.VideoWriter_fourcc(*"avc1")  
            out = cv2.VideoWriter(output_video_filename, fourcc, 30, (final_width, final_height))

            for frame in recording_frames:
                out.write(frame)

            out.release()

            #Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            metadata_entry = {
                "video_file": output_video_filename,
                "timestamp": timestamp,
                "intruder_position": intruder_position,
                "intruder_type": intruder_type
            }

            #Save metadata to a JSON file
            metadata_filename = f"{output_folder}/metadata.json"
            with open(metadata_filename, "w") as f:
                json.dump(metadata_entry, f)
  

            #Show screen notification 
            st.toast("Intruder detected! New recordings has been added.", icon=":material/update:")

            #Send email notification
            _ = send_email_alert(
                sender_email=sender_email,
                sender_password=sender_password,
                recipient_email=recipient_email,
                intruder_type=intruder_type,
                position=intruder_position,
                timestamp=timestamp
            )

            #Reset for next detection
            recording_frames = []
            movement_detected = False
            frame_count = 0

#Release Camera
camera.release()
