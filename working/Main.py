from Accelerometer import Accelerometer
from LEDController import LEDController
import time, math
import datetime

number_leds = 77
calibration_samples = 60
tolerance = 1.0
sleep_time = 0.01

LEDS = LEDController(number_leds)
Accel = Accelerometer(calibration_samples, tolerance, sleep_time)

animations = [
              LEDS.rainbow_cycle,
              LEDS.single_looping,
              LEDS.loading_bar,
              LEDS.fillRed,
              LEDS.fillBlue,
              LEDS.fillGreen,
                ]
LEDS.AttachAnimations(animations)

print("Starting Detection")
while True:
    if not Accel.CheckVibration():
        LEDS.RunAnimation()
    else:
        print("Hit Detected")
        Accel.Calibrate(calibration_samples)
        LEDS.changeAnimations()
    # time.sleep(0.05)
