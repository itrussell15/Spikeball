import time
import math, random
import smbus
from enum import IntEnum

class Accelerometer:

    def __init__(self, cal_samples, tol, sleep_time):
        self._calVals = {"x": 0, "y": 0, "z": 0}
        self._Accel = AccelLLC()
        self._sleep_time = sleep_time
        self.idealR = math.sqrt(1**2 + 1**2 + 1**2)
        self.tol = tol
        self.Calibrate(cal_samples)

    def Calibrate(self, samples):
        print("Calibrating")
        vals = {"x": 0, "y": 0, "z": 0}
        for i in range(samples):
            curr = self.CurrentVals()
            vals["x"] += curr["x"]
            vals["y"] += curr["y"]
            vals["z"] += curr["z"]
            time.sleep(self._sleep_time)
        calVals = {"x": 0, "y": 0, "z": 0}
        for i in vals:
            calVals[i] = vals[i] / samples
        self._calVals = calVals

    def CurrentVals(self):
        x = self._Accel.read_x_accel()
        y = self._Accel.read_y_accel()
        z = self._Accel.read_z_accel()
        return {"x": x, "y": y, "z": z}

    def showValues(self):
        x = self._Accel.read_x_accel(self._calVals["x"])
        y = self._Accel.read_y_accel(self._calVals["y"])
        z = self._Accel.read_z_accel(self._calVals["z"])
        print("X: {:.2f} Y: {:.2f} Z: {:.2f}".format(x, y, z))

    # Combination of all the axes
    def getResultant(self):
        R = self._Accel.read_x_accel(self._calVals["x"]) ** 2
        R += self._Accel.read_y_accel(self._calVals["y"]) ** 2
        R += self._Accel.read_z_accel(self._calVals["z"]) ** 2
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

class AccelLLC:
	def __init__(self):
		self._bus = smbus.SMBus(1)
		self._addr = 0x68
		self.MPU_Init()
		#Full scale range +/- 250 degree/C as per sensitivity scale factor
		self._calVal = 16384.0

	def MPU_Init(self):
		#write to sample rate register
		self._bus.write_byte_data(self._addr, self.Registers.SMPLRT_DIV, 7)

		#Write to power management register
		self._bus.write_byte_data(self._addr, self.Registers.PWR_MGMT_1, 1)

		#Write to Configuration register
		self._bus.write_byte_data(self._addr, self.Registers.CONFIG, 0)

		#Write to Gyro configuration register
		self._bus.write_byte_data(self._addr, self.Registers.GYRO_CONFIG, 24)

		#Write to interrupt enable register
		self._bus.write_byte_data(self._addr, self.Registers.INT_ENABLE, 1)

	def _read_raw_data(self, addr):
		#Accelero and Gyro value are 16-bit
	        high = self._bus.read_byte_data(self._addr, addr)
	        low = self._bus.read_byte_data(self._addr, addr+1)

	        #concatenate higher and lower value
	        value = ((high << 8) | low)

	        #to get signed value from mpu6050
	        if(value > 32768):
	                value = value - 65536
	        return value

	class Registers(IntEnum):
		#some MPU6050 Registers and their Address
		PWR_MGMT_1   = 0x6B
		SMPLRT_DIV   = 0x19
		CONFIG       = 0x1A
		GYRO_CONFIG  = 0x1B
		INT_ENABLE   = 0x38
		ACCEL_XOUT_H = 0x3B
		ACCEL_YOUT_H = 0x3D
		ACCEL_ZOUT_H = 0x3F
		GYRO_XOUT_H  = 0x43
		GYRO_YOUT_H  = 0x45
		GYRO_ZOUT_H  = 0x47

	def read_x_accel(self, cal_val = 1):
		return self._read_raw_data(self.Registers.ACCEL_XOUT_H) / cal_val

	def read_y_accel(self, cal_val = 1):
		return self._read_raw_data(self.Registers.ACCEL_YOUT_H) / cal_val

	def read_z_accel(self, cal_val = 1):
		return self._read_raw_data(self.Registers.ACCEL_ZOUT_H) / cal_val

	def read_x_gyro(self, cal_val = 1):
		return self._read_raw_data(self.Registers.GYRO_XOUT_H) / cal_val

	def read_y_gyro(self, cal_val = 1):
		return self._read_raw_data(self.Registers.GYRO_YOUT_H) / cal_val

	def read_z_gyro(self, cal_val = 1):
		return self._read_raw_data(self.Registers.GYRO_ZOUT_H) / cal_val
