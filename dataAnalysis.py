#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:09:45 2022

@author: schmuck
"""

import pandas as pd
import matplotlib.pyplot as plt
import math

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

fig1, axes1 = plt.subplots(nrows = 2, ncols = 1)
axes1[0].title.set_text("Net")
net[(net.index > start) & (net.index < stop)][interested].plot(ax = axes1[0])
axes1[1].title.set_text("Rim")
rim[(rim.index > start) & (rim.index < stop)][interested].plot(ax = axes1[1])

#Need to implement some sort of working detection system for this.
print("Net Min/Max Ratio: {:.2f}".format(abs(net["resultant"].max()/net["resultant"].min())))
print("Rim Min/Max Ratio: {:.2f}".format(abs(rim["resultant"].max()/rim["resultant"].min())))

