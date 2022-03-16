import smbus
from enum import IntEnum
import math
from time import sleep          #import

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
