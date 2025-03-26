import gpiod
import time

# Replace with the appropriate line number for your sensor.
# For example, if your sensor is connected to GPIO pin 21, you need to map it correctly.
# The mapping between BCM numbering and the gpiochip lines may differ.
sensor_line_number = 21  # Adjust as necessary

# Open the default gpiochip (usually gpiochip0)
chip = gpiod.Chip('gpiochip0')

# Request the line as input
line = chip.get_line(sensor_line_number)
line.request(consumer='soil_sensor', type=gpiod.LINE_REQ_DIR_IN)

try:
    while True:
        value = line.get_value()
        if value:
            print("Sensor reads LOW (dry)")
        else:
            print("Sensor reads High (wet)")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    line.release()
