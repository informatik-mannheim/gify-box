#!/bin/bash 

cd /home/innospace/gify-box/src/client
echo "$(date) - Startversuch" >> /home/innospace/gify-box/log.log


# Disable screen saver and screen blanking
xset s off
xset -dpms


# Start the program
sudo /home/innospace/gify-box/venv/bin/python /home/innospace/gify-box/src/client/single_instance.py >> /home/innospace/gify-box/log.log 2>&1
cd ../..
