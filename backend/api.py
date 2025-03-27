from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import datetime
import requests
from config import config  
import pyodbc
import bme680
import gpiod
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

app = FastAPI()


# Retrieve Azure endpoints and API keys from config
plant_identification_url = config.tokens.plant_prediction_url
plant_identification_api_key = config.tokens.plant_prediction_key
plant_disease_id_url = config.tokens.plant_diseases_prediction_url
plant_disease_id_api_key = config.tokens.plant_diseases_prediction_key

# Set headers for the prediction requests
headers_plant_id = {
    "Prediction-Key": plant_identification_api_key,
    "Content-Type": "application/octet-stream"
}

headers_plant_disease_id = {
    "Prediction-Key": plant_disease_id_api_key,
    "Content-Type": "application/octet-stream"
}

# Folder to store captured photos (optional)
output_folder = 'photos'
os.makedirs(output_folder, exist_ok=True)

@app.post("/predict")
def predict(image: UploadFile = File(...)):
    """
    Endpoint to receive an image file and perform predictions for plant identification and plant disease detection.
    """
    # Create a timestamped filename for the incoming image
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.jpg"
    file_path = os.path.join(output_folder, filename)
    
    # Save the uploaded image
    try:
        with open(file_path, "wb") as f:
            f.write(image.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")
    
    # Read the saved image in binary mode
    try:
        with open(file_path, "rb") as f:
            image_bytes = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read image: {str(e)}")
    
    try:
        # Send image for plant identification
        response_plant_id = requests.post(
            plant_identification_url,
            headers=headers_plant_id,
            data=image_bytes
        )
        response_plant_id.raise_for_status()
        prediction_plant_id = response_plant_id.json()

        # Send image for plant disease identification
        response_plant_disease_id = requests.post(
            plant_disease_id_url,
            headers=headers_plant_disease_id,
            data=image_bytes
        )
        response_plant_disease_id.raise_for_status()
        prediction_plant_disease_id = response_plant_disease_id.json()
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    
    # Process predictions for plant identification
    predictions_list_plant_id = prediction_plant_id.get("predictions", [])
    if predictions_list_plant_id:
        top_prediction_plant_id = max(predictions_list_plant_id, key=lambda x: x["probability"])
        plant_result = {
            "tagName": top_prediction_plant_id["tagName"],
            "probability": top_prediction_plant_id["probability"]
        }
    else:
        plant_result = {"error": "No predictions returned for plant identification."}
    
    # Process predictions for plant disease identification
    predictions_list_plant_disease_id = prediction_plant_disease_id.get("predictions", [])
    if predictions_list_plant_disease_id:
        top_prediction_plant_disease_id = max(predictions_list_plant_disease_id, key=lambda x: x["probability"])
        disease_result = {
            "tagName": top_prediction_plant_disease_id["tagName"],
            "probability": top_prediction_plant_disease_id["probability"]
        }
    else:
        disease_result = {"error": "No predictions returned for plant disease identification."}
    
    # Combine both prediction results and return as JSON
    result = {
        "plant_identification": plant_result,
        "plant_disease_identification": disease_result,
        "filename": filename
    }
    
    return JSONResponse(content=result)

###################################################################################################

# Database connection string
connection_string = (
    "Driver={FreeTDS};"
    "Server=root-project.database.windows.net;"
    "Port=1433;"
    "Database=pi;"
    "Uid=u;"
    "Pwd=ItIsKey!;"
    "TDS_Version=7.4;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

# Initialize the BME680 sensor
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Sensor configuration
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Initialize soil moisture sensor via gpiod
sensor_line_number = 21
chip = gpiod.Chip('gpiochip0')
line = chip.get_line(sensor_line_number)
line.request(consumer='soil_sensor', type=gpiod.LINE_REQ_DIR_IN)

app = FastAPI()

@app.get("/read-sensor")
def read_sensor_data():
    """
    Reads sensor data, inserts it into the database, and returns the inserted values.
    """
    # Establish database connection
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to the database: {e}")

    try:
        # Read sensor data once
        if sensor.get_sensor_data():
            timestamp = datetime.now()
            temperature = sensor.data.temperature
            pressure = sensor.data.pressure
            air_humidity = sensor.data.humidity
            soil_moisture = line.get_value()
            ph = None
            air_quality = None

            # Log sensor readings (optional)
            output = '{0:.2f} C, {1:.2f} hPa, {2:.2f} %RH'.format(
                temperature, pressure, air_humidity)
            print(output)

            insert_query = """
            INSERT INTO SensorData (
                Timestamp,
                SoilMoisture,
                AirHumidity,
                Temperature,
                Pressure,
                pH,
                AirQuality
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(
                insert_query,
                (timestamp, soil_moisture, air_humidity, temperature, pressure, ph, air_quality)
            )
            conn.commit()

            result = {
                "Timestamp": timestamp.isoformat(),
                "SoilMoisture": soil_moisture,
                "AirHumidity": air_humidity,
                "Temperature": temperature,
                "Pressure": pressure,
                "pH": ph,
                "AirQuality": air_quality,
                "message": "Data inserted successfully!"
            }
        else:
            result = {"message": "Sensor data not available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sensor data: {e}")
    finally:
        cursor.close()
        conn.close()

    return result

###########################################################################################################
# Azure OpenAI settings
endpoint = "https://plant-tip.openai.azure.com/openai/deployments/gpt-4o-mini"
model_name = "gpt-4o-mini"
openai_key = config.tokens.azure_openai_key

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(openai_key),
)

@app.get("/advise")
def get_advice(
    plant_type: str = "lemon tree",
    plant_disease: str = None,
    soil_humidity: float = 0.3,
    air_humidity: float = 0.2,
    temperature: float = 23.0,
    soil_pH: float = 5.0
):
    """
    Endpoint to get plant care advice based on input parameters.
    All parameters are optional.
    """
    try:
        # Build the user message using the provided parameters.
        user_message = f"My {plant_type} is showing signs of stress. "
        if plant_disease:
            user_message += f"It is also affected by {plant_disease}. "
        user_message += (
            f"The soil humidity is {soil_humidity}, air humidity is {air_humidity}, "
            f"soil pH is {soil_pH} and the temperature is {temperature}°C. "
            "Can you provide one advice?"
        )

        response = client.complete(
            messages=[
                SystemMessage(content=(
                    "You are a helpful home plant adviser who provides expert care tips for indoor plants. "
                    "Please provide exactly three pieces of advice. "
                    "Each piece of advice should be a short sentence ending with a relevant emoji."
                )),
                UserMessage(content=user_message)
            ],
            max_tokens=150,
            temperature=1.0,
            top_p=1.0,
            model=model_name
        )

        advice = response.choices[0].message.content
        return {"advice": advice}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
