import subprocess
import datetime
import time
import os

outputFolder = 'photos'

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

while True:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(outputFolder,f"photo_{timestamp}.jpg")
    subprocess.run(["libcamera-still", "--rotation", "180", "-o", filename] ) 
    time.sleep(3600)