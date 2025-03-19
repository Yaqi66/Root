import pyodbc
from datetime import datetime

# 1. Define your connection string
#    - Update the server name if yours differs (e.g., root-project.database.windows.net).
#    - Use the same 'Uid' and 'Pwd' you set when creating the login.
connection_string = (
    "Driver={FreeTDS};"
    "Server=root-project.database.windows.net;"
    "Port=1433;"
    "Database=pi;"
    "Uid=u;"
    "Pwd=ItIsKey@2025;"
    "TDS_Version=7.4;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)



try:
    # 2. Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # 3. Prepare data to insert
    #    Replace these sample values with real sensor readings if needed
    timestamp = datetime.now()
    soil_moisture = 1        # 1 for wet, 0 for dry
    air_humidity = 55.2      # e.g., 55.2% humidity
    temperature = 22.5       # e.g., 22.5 °C
    pressure = 1012.90       # e.g., 1012.90 hPa
    ph = 6.8                 # example pH reading
    air_quality = 42         # example integer for air quality

    # 4. Build your INSERT statement
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

    # 5. Execute the query with parameter values
    cursor.execute(
        insert_query,
        (timestamp, soil_moisture, air_humidity, temperature, pressure, ph, air_quality)
    )
    conn.commit()

    # 6. Close the cursor and connection
    cursor.close()
    conn.close()

    print("Data inserted successfully!")

except pyodbc.Error as e:
    print("Error connecting to the database:", e)
