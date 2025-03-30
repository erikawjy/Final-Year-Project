# Final-Year-Project
Indoor Home Surveillance System

This project is an indoor home security system that uses motion detetcion to identify intruders and send real-time alerts. When the system captures movement, details of the intruder and video recordings will be uploaded to the web dashboard for users to view. 

## Pre-requisites

### Installation
pip install -r requirements.txt
- Create a new python .env file to store email variables

### Email Setup for Nofications
- Create a .env file
- Go the google and click on 'manage your google account'
- Click on security and ensure that 2FA has been set up, otherwise set it up
- Once 2FA is set up, you will need to create an app password. This password will be needed in your .env file for sending alerts

- Type 'app passwords' in the search ba
- Key in a name for your password and note down the 16 character password
- In the .env file, add in the following

  ``` SENDER_EMAIL = 'your gmail address' ```
  ``` SENDER_PASSWORD = 'your app password created earlier' ```
(Do not include the ' ' at the sides)
 
### App variables - To be customized
- set recipient_email = '-gmail address that you want to send notifications to-'
- final_width = 1280 # size of the video display, dont need to change
- final_height = 720 # size of the video display, dont need to change
- binary_threshold = 100 #Change this according to different lighting conditions
- min_contour_area_to_trigger_detection = 10000 #To change the minimum bounding box area required to trigger detection
- max_small_object_area = 2500 #Threshold to determin is the object is small or big

## To run the app, key this into the terminal
```streamlit run Home.py```

