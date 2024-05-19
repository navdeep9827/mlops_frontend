import streamlit as st
import requests
import cv2
import numpy as np
import base64
from PIL import Image
import subprocess
import os
import time

# Function for starting Flask server
def start_flask():
    # Command for starting the Flask server
    command = ["python", "app.py"]
    flask_process = subprocess.Popen(command)
    return flask_process

# Starting the Flask server
flask_process = start_flask()

# Waiting for the Flask server to start
time.sleep(3)

st.title("Indian Sign Language Recognition")

# Setting up webcam capture
stframe = st.empty()
video_capture = cv2.VideoCapture(0)

def send_frame_to_flask(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = base64.b64encode(buffer).decode('utf-8')
    try:
        response = requests.post('http://localhost:5000/predict', json={'data': frame_bytes})
        response.raise_for_status()
        return response.json()['prediction']
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Flask server: {e}")
        return None

while True:
    ret, frame = video_capture.read()
    if not ret:
        st.write("Failed to capture video")
        break
    
    # Displaying the captured frame
    stframe.image(frame, channels="BGR")

    # Sending frame to Flask for prediction
    prediction = send_frame_to_flask(frame)
    if prediction is not None:
        st.write(f"Prediction: {prediction}")

video_capture.release()

# Terminating the flask process when streamlit is stopped
flask_process.terminate()
