import time
import bme680

try:
    # Initialize the sensor with the default I2C address (0x77)
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except Exception as e:
    print("Error initializing sensor:", e)
    exit(1)

# Configure oversampling settings
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# Enable gas sensor measurement (if needed)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print("Starting sensor read loop...")

while True:
    if sensor.get_sensor_data():
        temperature = sensor.data.temperature
        pressure = sensor.data.pressure
        humidity = sensor.data.humidity
        gas_resistance = sensor.data.gas_resistance

        print(f"Temperature: {temperature:.2f} °C")
        print(f"Pressure: {pressure:.2f} hPa")
        print(f"Humidity: {humidity:.2f} %")
        print(f"Gas Resistance: {gas_resistance:.2f} Ω")
        print("---------------------------")
    else:
        print("Failed to get sensor data")
    time.sleep(1)
