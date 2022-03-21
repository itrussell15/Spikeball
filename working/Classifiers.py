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
