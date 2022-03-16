from LowLevelSense import AccelLLC
import time, math
import board, neopixel

class Control:

    def __init__(self, samples, num_leds):
        self.sleep_time = 0.1 #Animation timer
        self.hit_color = (255,0,0)
        self._num_samples = samples

        self.accel = Accelerometer()
        self.LED = LEDController(num_leds)
        self.CalibrateSensor(self._num_samples)
        time.sleep(self.sleep_time)
        self.animationPosition = 0

    def CalibrateSensor(self, samples):
        print("Calibrating")
        vals = {"x": 0, "y": 0, "z": 0}
        self.LED.calibrationRing(0, samples)
        for i in range(samples):
            curr = self.accel.CurrentVals()
            vals["x"] += curr["x"]
            vals["y"] += curr["y"]
            vals["z"] += curr["z"]

            time.sleep(0.05)
        calVals = {"x": 0, "y": 0, "z": 0}
        for i in vals:
            calVals[i] = vals[i] / samples
        self.accel.set_calVals(calVals)

    def DetectVibration(self):
        if self.accel.CheckVibration():
            print("Hit Detected")
            time.sleep(self.sleep_time)
            self.CalibrateSensor(self._num_samples)
            self.animationPosition = 0
        else:
            if self.animationPosition >= self.LED.NUM_LEDS:
                self.animationPosition = 0
            self.LED.RunAnimation(self.animationPosition)
            self.animationPosition +=1

class LEDController:

    def __init__(self, num_leds, pin = board.D18):
        self.NUM_LEDS = num_leds
        self._control = neopixel.NeoPixel(pin, num_leds)
        self.fillRing((0,0,0))

    def calibrationRing(self, status, total):
        val = self.mapStatusToLeds(float(status/total))
        self.fillRing((255,0,0))
        # print(val)
        # for i in range(val):
        #     self._control[i] = (200, 200, 200)
        # self._control.show()

    def mapStatusToLeds(self, status_val):
        val = math.floor(status_val * self.NUM_LEDS)
        # print("NEW")
        return val if val > 0 else 0

    def fillRing(self, color = (255,0,0)):
        self._control.fill(color)

    def RunAnimation(self, pos):
        self._ThisAnimation(pos)

    def _ThisAnimation(self, pos):
        self._control.fill((0,0,0))
        self._control[pos] = ((200,200,200))


class Accelerometer:

    def __init__(self, cal_samples = 75, tol = 2.00):
        self.calVals = {"x": 0, "y": 0, "z": 0}
        self.Accel = AccelLLC()
        self.idealR = math.sqrt(1**2 + 1**2 + 1**2)
        self.tol = tol

    def set_calVals(self, vals):
        self.calVals = vals

    def CurrentVals(self):
        x = self.Accel.read_x_accel()
        y = self.Accel.read_y_accel()
        z = self.Accel.read_z_accel()
        return {"x": x, "y": y, "z": z}

    def showValues(self):
        x = self.Accel.read_x_accel(self.calVals["x"])
        y = self.Accel.read_y_accel(self.calVals["y"])
        z = self.Accel.read_z_accel(self.calVals["z"])
        print("X: {:.2f} Y: {:.2f} Z: {:.2f}".format(x, y, z))

    # Combination of all the axes
    def getResultant(self):
        R = self.Accel.read_x_accel(self.calVals["x"]) ** 2
        R += self.Accel.read_y_accel(self.calVals["y"]) ** 2
        R += self.Accel.read_z_accel(self.calVals["z"]) ** 2
        return math.sqrt(R)

    # Checks if inside allowed range
    def withinTol(self, R):
        upper = self.idealR * (1 + self.tol)
        lower = self.idealR * (1 - self.tol)
        # print("{:2f} < {:2f} < {:.2f}".format(lower, R, upper))
        return R < upper and R > lower

    def CheckVibration(self):
        R = self.getResultant()
        return not self.withinTol(R)
