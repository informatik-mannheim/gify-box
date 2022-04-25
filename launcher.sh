#!/bin/sh 
cd src/client

# Disable sreen saver and screen blanking
xset s off
xset -dpms

# Start the program
sudo DISPLAY=:0 python single_instance.py
cd ../.. 

