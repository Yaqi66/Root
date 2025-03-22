import pyodbc
from datetime import datetime
import bme680
import time
import gpiod

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

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

temperature = sensor.data.temperature
pressure = sensor.data.pressure
humidity = sensor.data.humidity

sensor_line_number = 21 
chip = gpiod.Chip('gpiochip0')
line = chip.get_line(sensor_line_number)
line.request(consumer='soil_sensor', type=gpiod.LINE_REQ_DIR_IN)

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    while True:
        if sensor.get_sensor_data():
            timestamp = datetime.now()
            temperature = sensor.data.temperature
            pressure = sensor.data.pressure
            air_humidity = sensor.data.humidity
            soil_moisture = line.get_value()
            ph = none
            air_quality = none

            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity)
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

        # 6. Close the cursor and connection
        cursor.close()
        conn.close()

        print("Data inserted successfully!")
        
        time.sleep(1)

except pyodbc.Error as e:
    print("Error connecting to the database:", e)
