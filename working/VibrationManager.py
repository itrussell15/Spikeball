from LowLevelSense import AccelLLC
import time
import math, random

class Control:

    def __init__(self, samples, num_leds):
        self.hit_color = (255, 0, 0)
        self._num_samples = samples

        self.accel = Accelerometer()
        self.CalibrateSensor(self._num_samples)

    # def CalibrateSensor(self, samples):


    def DetectVibration(self):
        return self.accel.CheckVibration()

class LEDController:

    def __init__(self, num_leds):
        import board

        self.NUM_LEDS = num_leds
        self._control = neopixel.NeoPixel(board.D18, num_leds)

        self.fill((0, 0, 0))
        self._control.show()

        self._pos = 0
        self._index = 0
        self._flag = 0

    def AttachAnimations(self, animations):
        self._animations = _animations
        random.shuffle(self._animations )

    def changeAnimations(self):
        if self._index <= len(self._animations) - 1:
            self._index +=1
        else:
            self._index = 0
        self._control.fill((0, 0, 0))

    def RunAnimation(self):
        self._animations[self._animationIndex](self._pos)
        if self._pos <= 255:
            self._pos += 1
        else:
            self._pos = 0
        self._control.show()

    def _wheel(self, pos):
        ORDER = neopixel.GRB
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(self, pos):
        # for j in range(255):
        print("Rainbow Cycle")
        for i in range(self.num_leds):
            pixel_index = (i * 256 // self.num_leds) + pos
            self.control[i] = self._wheel(pixel_index & 255)
        self.control.show()

    def loading_bar(self, pos):
        print("Loading Bar")
        mapped_pos = self._mapValue(pos)
        if mapped_pos < self.num_leds:
            if flag == 0:
                self.control[mapped_pos] = (255, 255, 255)
            else:
                self.control[self.num_leds - mapped_pos] = (255,255,255)
        else:
            self._flag = 0 if self._flag == 1 else 0

    def single_looping(self, pos):
        print("Single Looping")
        self.control.fill((0, 0, 0))
        self.control[pos] = ((200, 200, 200))

    def fillRed(self, pos):
        print("Fill Red")
        self.control.fill(255, 0, 0)

    def fillWhite(self, pos):
        print("Fill White")
        self.control.fill(255, 255, 255)

    def fillBlue(self, pos):
        print("Fill Blue")
        self.control.fill(0, 0, 255)

    def fillGreen(self, pos):
        print("Fill Green")
        self.control.fill(0, 255, 0)

    def breathingWhite(self, pos):
        print("Fill White")
        self.control.fill(i, i, i)

    # Returns a mapped value from 255 to the number of leds in the strip
    def _mapValue(self, value):
        scaled = float(value) / float(255.0)
        return math.floor(scaled * self.num_leds)

class Accelerometer:

    def __init__(self, cal_samples, tol):
        self._calVals = {"x": 0, "y": 0, "z": 0}
        self.Accel = AccelLLC()
        self.idealR = math.sqrt(1**2 + 1**2 + 1**2)
        self.tol = tol

    def Calibrate(self, samples):
        print("Calibrating")
        vals = {"x": 0, "y": 0, "z": 0}
        for i in range(samples):
            curr = self.CurrentVals()
            vals["x"] += curr["x"]
            vals["y"] += curr["y"]
            vals["z"] += curr["z"]
            time.sleep(0.05)
        calVals = {"x": 0, "y": 0, "z": 0}
        for i in vals:
            calVals[i] = vals[i] / samples
        self._calVals = calVals

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
        # print(R)
        return not self.withinTol(R)

class BounceClassifer:

    def __init__(self, tol, ratio_threshold, response=None, samples=10):
        self.samples = samples
        self.tol = tol
        self.ratio_threshold = ratio_threshold

        if response:
            self.response = response
        else:
            self.response = self.collectData

        self._globalCounter = 0

        self.peak = 0
        self.counter = 0
        self.flag = False
        self.inspection_max = 0

        self._output = {}

    def running(self, value):
        output = False
        if self.flag:
            # TODO check why inspection value isn't getting set before ratio
            if self.counter < self.samples:
                self.counter += 1
                self._checkInspection(value)
            else:
                ratio = abs(self.peak)/abs(self.inspection_max)
                # Trigger point of a hit
                if ratio > self.ratio_threshold:
                    # self.response(ratio)
                    output = True
                self.counter = 0
                self.peak = 0
                self.flag = False
                self.inspection_max = 1
        self._checkPeak(value)
        self._globalCounter += 1
        return output

    def _checkPeak(self, value):
        if abs(value) > abs(self.tol):
            # print("HERE")
            if abs(value) > abs(self.peak):
                # print("Peak overwritten!")
                self.peak = value
                self.flag = True
                # self.inspection_max = 1

    def _checkInspection(self, value):
        if abs(value) > self.tol:
            if abs(value) > self.inspection_max:
                self.inspection_max = value

    def collectData(self, ratio):
        self._output.update({self._globalCounter: ratio})

    def getOutput(self):
        return self._output
