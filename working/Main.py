from VibrationManager import Control, Accelerometer
import time, math
import datetime

number_leds = 77
calibration_samples = 60

C = Control(calibration_samples, number_leds)
data = ""
print("Starting Detection")
for i in range(10000):
    val = C.accel.getResultant()
    data += "{:.2f}\n".format(val)
#     if not C.accel.withinTol(val):
#         print(val)
#     C.DetectVibration()
#     time.sleep(0.01)

with open("data.txt", "w") as f:
    f.write(data)
    f.close()
