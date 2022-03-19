from LowLevelSense import AccelLLC
import time
import math
import neopixel


class Control:

    def __init__(self, samples, num_leds):
        self.hit_color = (255, 0, 0)
        self._num_samples = samples

        self.accel = Accelerometer()
        self.LED = LEDController(num_leds)
        self.CalibrateSensor(self._num_samples)

    def CalibrateSensor(self, samples):
        print("Calibrating")
        vals = {"x": 0, "y": 0, "z": 0}
        self.LED.calibrationRing(0, samples)
        for i in range(samples):
            curr = self.accel.CurrentVals()
            vals["x"] += curr["x"]
            vals["y"] += curr["y"]
            vals["z"] += curr["z"]

            time.sleep(0.01)
        calVals = {"x": 0, "y": 0, "z": 0}
        for i in vals:
            calVals[i] = vals[i] / samples
        self.accel.set_calVals(calVals)

    def DetectVibration(self):
        return self.accel.CheckVibration()
        # if self.accel.CheckVibration():
        #     print("Hit Detected")
        #     time.sleep(self.sleep_time)
        #     self.CalibrateSensor(self._num_samples)
        #     self.animationPosition = 0
        # else:
        #     if self.animationPosition >= self.LED.NUM_LEDS:
        #         self.animationPosition = 0
        #     self.LED.RunAnimation(self.animationPosition)
        #     self.animationPosition += 1


class LEDController:

    def __init__(self, num_leds):
        import board
        import neopixel
        self.NUM_LEDS = num_leds
        self._control = neopixel.NeoPixel(board.D18, num_leds)
        self.fillRing((0, 0, 0))
        self._control.show()
        self._pos = 0
        self._animationIndex = 0
        self._myAnimations = self.AnimationController(self._control, self.NUM_LEDS)
        self._animations = [
            self._myAnimations.rainbow_cycle,
            self._myAnimations.loading_bar,
            self._myAnimations.single_looping,
            ]
        print("{} animations loaded".format(len(self._animations)))

    def calibrationRing(self, status, total):
        val = self.mapStatusToLeds(float(status/total))
        # Associate with some animations?

    def mapStatusToLeds(self, status_val):
        val = math.floor(status_val * self.NUM_LEDS)
        # print("NEW")
        return val if val > 0 else 0

    def fillRing(self, color=(255, 0, 0)):
        self._control.fill(color)

    def changeAnimations(self):
        if self._animationIndex >= len(self._animations) - 1:
            self._animationIndex = 0
        else:
            self._animationIndex += 1
        self._control.fill((0,0,0))

    def RunAnimation(self):
        print("Animation Running: {}".format(self._animationIndex))
        self._animations[self._animationIndex](self._pos)
        if self._pos <= 255:
            self._pos += 1
        else:
            self._pos = 0
    #
    # def _ThisAnimation(self, pos):
    #     self._control.fill((0, 0, 0))
    #     self._control[pos] = ((200, 200, 200))

    class AnimationController:

        def __init__(self, controller, leds):
            self.num_leds = leds
            self.control = controller

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
            for i in range(self.num_leds):
                pixel_index = (i * 256 // self.num_leds) + pos
                self.control[i] = self._wheel(pixel_index & 255)
            self.control.show()

        def loading_bar(self, pos):
            mapped_pos = self.mapValue(pos)
            print(mapped_pos)
            if mapped_pos < self.num_leds:
                self.control[mapped_pos] = (255, 255, 255)
            else:
                self.control.fill((0,0,0))

        def single_looping(self, pos):
            self.control.fill((0, 0, 0))
            mapped = self.mapValue(pos)
            if mapped <= self.num_leds - 1:
                self.control[mapped] = ((200, 200, 200))
            else:
                self.control.fill((0,0,0))

        # Returns a mapped value from 255 to the number of leds in the strip
        def mapValue(self, value):
            scaled = float(value) / float(255.0)
            return math.floor(scaled * self.num_leds)





class Accelerometer:

    def __init__(self, cal_samples=25, tol=2.0):
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
        #print(R)
        return not self.withinTol(R)





class BounceClassifer:

    def __init__(self, tol, ratio_threshold, response=None, samples=10, ):
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
