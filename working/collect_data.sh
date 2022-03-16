#!/bin/bash

echo "Collect Net!"
sudo python dataCollect.py
mv data/data.csv data/net.csv
sshpass -p "zacisa12" scp -r data/net.csv schmuck@192.168.0.57:/media/schmuck/SCHMUCK/Coding/Projects/Spikeball/working/data

echo "Collect Rim!"
sudo python dataCollect.py
mv data/data.csv data/rim.csv
sshpass -p "zacisa12" scp -r data/rim.csv schmuck@192.168.0.57:/media/schmuck/SCHMUCK/Coding/Projects/Spikeball/working/data
