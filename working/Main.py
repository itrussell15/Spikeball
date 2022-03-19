from VibrationManager import Control, Accelerometer, BounceClassifer
import time, math
import datetime

number_leds = 77
calibration_samples = 50
pos = 0

C = Control(calibration_samples, number_leds)

print("Starting Detection")
while True:
    if not C.DetectVibration():
        C.LED.RunAnimation()
    else:
        C.CalibrateSensor(calibration_samples)
        print("HERE")
        C.LED.changeAnimations()
    time.sleep(0.01)
