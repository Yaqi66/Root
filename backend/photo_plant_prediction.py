import subprocess
import datetime
import time
import os
import requests
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Folder to store captured photos
outputFolder = 'photos'
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# Azure Custom Vision endpoint and API key from environment variables
plant_identification_url = os.getenv("Plant-Prediction-url")
plant_identification_api_key = os.getenv("Plant-Prediction-Key")

plant_disease_id_url = os.getenv("Plant-Diseases-Prediction-url")
plant_disease_id_api_key = os.getenv("Plant-Diseases-Prediction-Key")

# Set headers for the request
headers_plant_id = {
    "Prediction-Key": plant_identification_api_key,
    "Content-Type": "application/octet-stream"
}

headers_plant_disease_id = {
    "Prediction-Key": plant_disease_id_api_key,
    "Content-Type": "application/octet-stream"
}

while True:
    # Capture photo with a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(outputFolder, f"photo_{timestamp}.jpg")
    subprocess.run(["libcamera-still", "--rotation", "180", "-o", filename])

    # Open the image file and read in binary mode
    with open(filename, "rb") as image_file:
        image_bytes = image_file.read()

    # Send the image to the Azure endpoint for prediction
    try:
        response_plant_id = requests.post(plant_identification_url, headers=headers_plant_id, data=image_bytes)
        response_plant_id.raise_for_status()  # Raises an HTTPError for bad responses
        prediction_plant_id = response_plant_id.json()

        response_plant_disease_id = requests.post(plant_disease_id_url, headers=headers_plant_disease_id, data=image_bytes)
        response_plant_disease_id.raise_for_status()  # Raises an HTTPError for bad responses
        prediction_plant_disease_id = response_plant_disease_id.json()

        # Extract predictions list from the JSON response
        print("plant name:")
        predictions_list_plant_id = prediction_plant_id.get("predictions", [])
        if predictions_list_plant_id:
            # Find the prediction with the highest probability
            top_prediction_plant_id = max(predictions_list_plant_id, key=lambda x: x["probability"])
            tag_name_plant_id = top_prediction_plant_id["tagName"]
            probability_plant_id = top_prediction_plant_id["probability"]
            print(f"Most likely prediction for {filename}: {tag_name_plant_id} ({probability_plant_id:.2%} confidence)")
        else:
            print(f"No predictions returned for {filename}.")

        #prediction for plant diseases
        print("disease:")
        predictions_list_plant_disease_id = prediction_plant_disease_id.get("predictions", [])
        if predictions_list_plant_disease_id:
            # Find the prediction with the highest probability
            top_prediction_plant_disease_id = max(predictions_list_plant_disease_id, key=lambda x: x["probability"])
            tag_name_plant_disease_id = top_prediction_plant_disease_id["tagName"]
            probability_plant_disease_id = top_prediction_plant_disease_id["probability"]
            print(f"Most likely prediction for {filename}: {tag_name_plant_disease_id} ({probability_plant_disease_id:.2%} confidence)")
        else:
            print(f"No predictions returned for {filename}.")

    except requests.exceptions.RequestException as e:
        print(f"Error during prediction: {e}")

    # Wait for 1 min before taking the next photo
    time.sleep(60)
