from VibrationManager import LEDController, Accelerometer
import time, math
import datetime

number_leds = 77
calibration_samples = 60
tolerance = 1.0

LEDS = LEDController(number_leds)
Aceel = Accelerometer(calibration_samples, tolerance)

animations = [
              LEDS.rainbow_cycle,
              LEDS.single_looping,
                ]

LEDS.AttachAnimations(animations)


print("Starting Detection")
while True:
    if not Accel.CheckVibration():
        LED.RunAnimation()
    else:
        Accel.Calibrate(calibration_samples)
        LED.changeAnimations()
    # time.sleep(0.05)
