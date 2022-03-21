#!/bin/bash

echo "Collect Net!"
sudo python dataCollect.py
mv data/data.csv data/net$1.csv
sshpass -p "zacisa12" scp -r data/net$1.csv schmuck@192.168.0.57:/media/schmuck/SCHMUCK/Coding/Projects/Spikeball/working/data/net
sudo rm data/net$1.csv

echo "Collect Rim!"
sudo python dataCollect.py
mv data/data.csv data/rim$1.csv
sshpass -p "zacisa12" scp -r data/rim$1.csv schmuck@192.168.0.57:/media/schmuck/SCHMUCK/Coding/Projects/Spikeball/working/data/rim
sudo rm data/rim$1.csv
