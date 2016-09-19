#!/bin/bash
clear
echo "=== Starting installation of GIF Box ==="

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as sudo!" 1>&2
   exit 1
fi


echo " -- START: Installing software using apt-get --"
sudo apt-get update && sudo apt-get upgrade

sudo apt-get install -y build-essential git python python-rpi.gpio python-dev python-pip libjpeg-dev python-serial python-imaging python-unidecode scons swig viewnior graphicsmagick

# install python requests
sudo pip install requests
echo " -- DONE:  Installing software using apt-get --"

# neopixel installation
echo " -- START: Installing Neopixel library --"
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
echo " -- DONE:  Installing Neopixel library --"

# project clone
echo " -- START: Cloning project --"
git clone https://github.com/gtRfnkN/photobooth.git
echo " -- DONE: Cloning project --"


echo " -- DONT FORGET TO DISABLED SCREEN BLANKING MANUALLY --"
echo " -- read and follow installation/screenblanking.txt! --"

echo "=== Finished installation of GIF Box ==="

echo ">>> Rebooting in 5 seconds <<<"
sleep 1
echo ">>> Rebooting in 4 seconds <<<"
sleep 1
echo ">>> Rebooting in 3 seconds <<<"
sleep 1
echo ">>> Rebooting in 2 seconds <<<"
sleep 1
echo ">>> Rebooting in 1 seconds <<<"
sleep 1
echo ">>>  Rebooting right now   <<<"
reboot