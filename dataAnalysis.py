#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:09:45 2022

@author: schmuck
"""

import pandas as pd
import matplotlib.pyplot as plt
import math
from working.VibrationManager import PeakClassifer

sample_num = 14
rolling = 15
start = 0
stop = 200
interested = ["Z_rolling", "Z_accel"]

def resultant(x):
    pre = (x["X_accel"] ** 2) + (x["Y_accel"] ** 2) + (x["Z_accel"] ** 2)
    return math.sqrt(pre)
    

net = pd.read_csv("working/data/net{}.csv".format(sample_num))
net.drop("Z_gyro", axis = 1, inplace = True)
net["resultant"] = net.apply(resultant, axis = 1)
net["Z_rolling"] = abs(net["Z_accel"].rolling(rolling).mean())

rim = pd.read_csv("working/data/rim{}.csv".format(sample_num))
rim["resultant"] = rim.apply(resultant, axis = 1)
rim["Z_rolling"] = abs(rim["Z_accel"].rolling(rolling).mean())
rim.drop("Z_gyro", axis = 1, inplace = True)

tol = 2
samples = 10

peak = 0
spike_flag = False
counter = 0
netClass = PeakClassifer(tol = 5, samples = 15)
rimClass = PeakClassifer(tol = 5, samples = 15)


for i in net["Z_accel"]:
    netClass.running(i)
for i in rim["Z_accel"]:
    rimClass.running(i)
    
netVals = netClass.getOutput()
rimVals = rimClass.getOutput()

print("Net {}".format(netVals))
print("Rim {}".format(rimVals))
            
def showHitLines(axis, values, data):
    for i in values:
        axis.vlines(x = i - samples, linestyle = "--", color = "k", ymin = data["Z_accel"].min(), ymax = data["Z_accel"].max())
        axis.vlines(x = i, linestyle = "--", color = "r", ymin = data["Z_accel"].min(), ymax = data["Z_accel"].max())
    

fig1, axes1 = plt.subplots(nrows = 2, ncols = 1)
axes1[0].title.set_text("Net")
net[(net.index > start) & (net.index < stop)][interested].plot(ax = axes1[0])
# axes1[0].vlines(x = list(netVals.keys())[0] - samples, linestyle = "--", color = "k", ymin = net["Z_accel"].min(), ymax = net["Z_accel"].max())
showHitLines(axes1[0], netVals, net)
axes1[1].title.set_text("Rim")
rim[(rim.index > start) & (rim.index < stop)][interested].plot(ax = axes1[1])
# axes1[1].vlines(x = list(rimVals.keys())[0] - samples, linestyle = "--", color = "k", ymin = rim["Z_accel"].min(), ymax = rim["Z_accel"].max())
showHitLines(axes1[1], rimVals, rim)

#Need to implement some sort of working detection system for this.
# print("Net Min/Max Ratio: {:.2f}".format(abs(net["Z_accel"].max()/net["Z_accel"].min())))
# print("Rim Min/Max Ratio: {:.2f}".format(abs(rim["Z_accel"].max()/rim["Z_accel"].min())))

