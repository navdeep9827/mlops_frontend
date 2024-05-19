import streamlit as st
import requests
import cv2
import numpy as np
import base64
import subprocess
import time

# Function for starting Flask server
def start_flask():
    command = ["python", "app.py"]
    flask_process = subprocess.Popen(command)
    return flask_process

# Starting the Flask server
flask_process = start_flask()

# Waiting for the Flask server to start
time.sleep(15)

st.title("Indian Sign Language Recognition")

# Setting up webcam capture
stframe = st.empty()
video_capture = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not video_capture.isOpened():
    st.error("Error: Could not open video stream.")
    flask_process.terminate()
    st.stop()

def send_frame_to_flask(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = base64.b64encode(buffer).decode('utf-8')
    try:
        response = requests.post('https://mlops-project-r08k.onrender.com/predict', json={'data': frame_bytes})
        response.raise_for_status()
        return response.json().get('prediction', None)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Flask server: {e}")
        return None

while True:
    ret, frame = video_capture.read()
    if not ret:
        st.error("Failed to capture video.")
        break
    
    # Displaying the captured frame
    stframe.image(frame, channels="BGR")

    # Sending frame to Flask for prediction
    prediction = send_frame_to_flask(frame)
    if prediction is not None:
        st.write(f"Prediction: {prediction}")
    else:
        st.write("No prediction received.")

# Releasing the video capture object
video_capture.release()

# Terminating the Flask process when Streamlit stops
flask_process.terminate()
