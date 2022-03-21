#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Accelerometer import AccelLLC
import time, csv

def CurrentVals():
    ax = accel.read_x_accel()
    ay = accel.read_y_accel()
    az = accel.read_z_accel()
    gx = accel.read_x_gyro()
    gy = accel.read_y_gyro()
    gz = accel.read_z_gyro()
    return {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz}

def CalibrateSensor(samples):
    vals = {"ax": 0, "ay": 0, "az": 0, "gx": 0, "gy": 0, "gz": 0}
    for i in range(samples):
        curr = CurrentVals()
        vals["ax"] += curr["ax"]
        vals["ay"] += curr["ay"]
        vals["az"] += curr["az"]
        vals["gx"] += curr["gx"]
        vals["gy"] += curr["gy"]
        vals["gz"] += curr["gz"]
        time.sleep(0.05)
    calVals = {"x": 0, "y": 0, "z": 0}
    for i in vals:
        calVals[i] = vals[i] / samples
    return calVals

accel = AccelLLC()
print("Calibrating")
calVals = CalibrateSensor(25)

print("Collect!")
output = []
for i in range(300):
    output.append([accel.read_x_gyro(calVals["gx"]) - 1, accel.read_y_gyro(calVals["gy"]) - 1, accel.read_z_gyro(calVals["gz"]) - 1,\
    accel.read_x_accel(calVals["ax"]) - 1, accel.read_y_accel(calVals["ay"]) - 1, accel.read_z_accel(calVals["az"]) - 1])
    time.sleep(0.01)

with open("data/data.csv", "w") as f:
    csv = csv.writer(f)
    csv.writerow(["X_gyro", "Y_gyro", "Z_gyro", "X_accel", "Y_accel", "Z_accel"])
    csv.writerows(output)
