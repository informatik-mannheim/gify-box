# Installation

This document describes the installation of the GifyBox on a Raspberry PI with Raspberry Pi OS (Bookworm). After installing the operating system, some additional steps are required.

## Display Orientation

With the newest Raspian versions, you can no longer change the display orientation using the `/boot/config.txt` file but have to do it with the `xrand` command.

```console
xrandr --output HDMI-1 --rotate inverted
```

Afterwards you can persist the setting in the display settings of the user interface.

## Taskbar
To enable the fullscreen preview later on, set the taskbar position to the bottom of the display. 
Right click the taskbar, select "Taskbar Preferences" and change the position from Top to Bottom. Additionally, change the size to small (16x16). 

## Enable Neopixel

The GifyBox uses Neopixel stripes for the visualization of the process.

Due to the fact that the library used for the Neopixel control (`rpi_ws281x`) uses some internal circuits of the computer, which are part of the audio interface, you have to disable the audio interface to enable the Neopixels.

Create a file `/etc/modprobe.d/snd-blacklist.conf` with the following content `blacklist snd_bcm2835`.

```console
sudo echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf
```


### Raspberry PI 3 / 4

If your are using a Raspberry PI 3 or 4, the serial interface is not readily available and you need to change some configuration options. The reason is that the Bluetooth chip uses the same UART component. Therefore, you have to disable Bluetooth to gain access to the RS232 port on `/dev/serial0`.

Please add the following lines to the end of the file `/boot/firmware/config.txt`:

```console
dtoverlay=disable-bt
enable_uart=1
```

Additionally, modify the file `/boot/firmware/cmdline.txt` and remove the serial console. If you do not remove it, the Raspberry will open a console on the freshly gained RS232 port, and you cannot use it for the printer.

The file may look like this:

```console
console=serial0,115200 console=tty1 root=PARTUUID=e8fef0a8-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

Delete the `console=serial0,115200` part to free the serial interface. After the removal the file looks like this:

```console
console=tty1 root=PARTUUID=e8fef0a8-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

Please keep in mind that you should not copy this line directly into your `cmdline.txt` because it contains information about the boot device. This may render your Raspberry PI unusable.

## Install additional system packages

Install the following packages:

* build-essential
* git
* scons
* swig
* viewnior
* graphicsmagick
* libopencv-dev
* python3-opencv

```console
sudo apt update
sudo apt install build-essential git scons swig viewnior graphicsmagick libopencv-dev python3-opencv
```

## Install the GifyBox software

Install the software from the GitHub repository.

```console
cd ~
git clone https://github.com/informatik-mannheim/gify-box.git
```

## Setup the python virtual environment
Starting in Raspberry Pi OS Bookworm, packages installed via pip must be installed into a Python virtual environment (venv).

Navigate into the cloned gify-box directory.
Create the virtual environment:
```console
cd gify-box
python -m venv venv --system-site-packages 
```

## Install the required Python packages:

First, activate the previously created virtual environment:
```console
source venv/bin/activate
```

Then install the required Python packages:
* qrcode
* imagio
* pyserial
* requests
* Pillow
* rpi_ws281x

```console
pip install qrcode[pil] imageio pyserial requests Pillow rpi_ws281x
```

## Start the software on the box:
The software client must be run as *root* to have access to the hardware, therefore you can use the starter script in the main directory of the project. Although, it is for the client only, we placed it there to make running the client as easy as possible.

```
cd gify-box
./launcher.sh
```


# Prevent Display Blanking

By default, the display will be turned off after a few moments. You won't notice this when the preview is open, because it overlays the blank screen somehow. But the replay of the GIF does not work. So we need to address and fix that.

Turing of the display blanking is done automatically by the [start script](../../launcher.sh). If you want to do it manually, enter the following two commands into the terminal:

```console
xset s off
xset -dpms
```
