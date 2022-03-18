from VibrationManager import Control, Accelerometer, BounceClassifer
import time, math
import datetime

number_leds = 77
calibration_samples = 60
pos = 0

C = Control(calibration_samples, number_leds)
classifier = BounceClassifer(tol = 5, ratio_threshold=2.5)

print("Starting Detection")
while True:
    vals = C.accel.CurrentVals()
    if classifier.running(vals["z"]):
        print("Hit Detected!")
        C.CalibrateSensor(calibration_samples)
    else:
        C.LED.RunAnimation(pos)
        if pos >= number_leds - 1:
            pos = 0
        else:     
            pos += 1
        
    # time.sleep(0.01)
