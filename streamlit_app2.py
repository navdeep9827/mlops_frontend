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

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

def send_image_to_flask(image):
    # Convert image to JPEG format
    img = Image.open(image)
    img = img.convert('RGB')
    img.save("temp.jpg", format="JPEG")

    # Read JPEG image and encode it to base64
    with open("temp.jpg", "rb") as file:
        image_bytes = base64.b64encode(file.read()).decode("utf-8")

    # Send image to Flask for prediction
    try:
        response = requests.post('http://localhost:5000/predict', json={'data': image_bytes})
        response.raise_for_status()
        return response.json()['prediction']
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Flask server: {e}")
        return None

# Display prediction
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    prediction = send_image_to_flask(uploaded_file)
    if prediction is not None:
        st.write(f"Prediction: {prediction}")

# Terminating the flask process when streamlit is stopped
flask_process.terminate()
