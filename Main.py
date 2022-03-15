from VibrationManager import Control
import time, math
import datetime

number_leds = 60
calibration_samples = 60

C = Control(calibration_samples, number_leds)

print("Starting Detection")
while True:
    C.DetectVibration()
    time.sleep(0.05)
