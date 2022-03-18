#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:09:45 2022

@author: schmuck
"""

import pandas as pd
import matplotlib.pyplot as plt
import math, os
from working.VibrationManager import BounceClassifer

def showHitLines(axis, values, data):
    for i in values:
        axis.vlines(x = i - samples, linestyle = "--", color = "k", ymin = data["Z_accel"].min(), ymax = data["Z_accel"].max())
        axis.vlines(x = i, linestyle = "--", color = "r", ymin = data["Z_accel"].min(), ymax = data["Z_accel"].max())

interested = ["Z_accel"]

netFiles = [i for i in os.listdir("working//data//net")]
rimFiles = [i for i in os.listdir("working//data//rim")]
counter = 0
rolling = 15

for net, rim in zip(netFiles, rimFiles):
    counter += 1
    print("Running Test {}".format(counter))
    net_df = pd.read_csv("working//data/net//{}".format(net))
    # net_df.drop("Z_gyro", axis = 1, inplace = True)
    # net_df["Z_rolling"] = abs(net["Z_accel"].rolling(rolling).mean())
    
    rim_df = pd.read_csv("working//data//rim//{}".format(rim))
    # rim_df.drop("Z_gyro", axis = 1, inplace = True)
    # rim["Z_rolling"] = abs(rim["Z_accel"].rolling(rolling).mean())
    
    tol = 5
    samples = 10

    netClass = BounceClassifer(ratio_threshold = 2.5, tol = tol, samples = samples)
    rimClass = BounceClassifer(ratio_threshold = 2.5, tol = tol, samples = samples)

    for i in net_df["Z_accel"]:
        netClass.running(i)
    for i in rim_df["Z_accel"]:
        rimClass.running(i)
    
    netVals = netClass.getOutput()
    rimVals = rimClass.getOutput()

    print("Net {}".format(netVals))
    print("Rim {}".format(rimVals))
            
    fig1, axes1 = plt.subplots(nrows = 2, ncols = 1)
    fig1.suptitle("Net {} Rim {}".format(netVals, rimVals))
    axes1[0].title.set_text("Net")
    net_df[(net_df.index > 0) & (net_df.index < len(net_df))][interested].plot(ax = axes1[0])
    showHitLines(axes1[0], netVals, net_df)
    axes1[1].title.set_text("Rim")
    rim_df[(rim_df.index > 0) & (rim_df.index < len(rim_df))][interested].plot(ax = axes1[1])
    showHitLines(axes1[1], rimVals, rim_df)


