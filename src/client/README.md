# Installation

This document describes the installation of the GifyBox on a Raspberry PI. After installing the operating system, some additional steps are required.

## Display Orientation

With the newest Raspian versions, you can no longer change the display orientation using the `/boot/config.txt` file but have to do it with the `xrand` command.

```console
$ xrandr --output HDMI-1 --rotate inverted
```

Afterwards you can persist the setting in the display settings of the user interface.


## Enable the Camera

If you use the standard Raspberry PI camera, you have to enable it in the configuration of the computer.

Start the configuration program:

```console
$ sudo raspi-config
```

Open the *Interfacing Options* and enable the legacy camera.


## Enable Neopixel

The GifyBox uses Neopixel stripes for the visualization of the process.

Due to the fact that the library used for the Neopixel control (`rpi_ws281x`) uses some internal circuits of the computer, which are part of the audio interface, you have to disable the audio interface to enable the Neopixels.

Create a file `/etc/modprobe.d/snd-blacklist.conf` with the following content `blacklist snd_bcm2835`.

```console
$ sudo echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf
```


### Raspberry PI 3

If your are using a Raspberry PI 3, the serial interface is not readily available, but you need to change some configuration options. The reason is that the Bluetooth chip uses the same UART component. Therefore, you have to disable Bluetooth to gain access to the RS232 port on `/dev/serial0`.

Please add the following lines to the end of the file `/boot/config.txt`:

```console
dtoverlay=disable-bt
core_freq=250
enable_uart=1
```

Additionally, modify the file `/boot/cmdline.txt` and remove the serial console. If you do not remove it, the Raspberry will open a console on the freshly gained RS232 port, and you cannot use it for the printer.

The file may look like this:

```console
console=serial0,115200 console=tty1 root=PARTUUID=e8fef0a8-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

Delete the `console=serial0,115200` part to free the serial interface. After the removal the file looks like this:

```console
console=tty1 root=PARTUUID=e8fef0a8-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```

Please keep in mind that you should not copy this line directly into your `cmdline.txt` because it contains information about the boot device. This may render your Raspberry PI unusable.


## Install additional packages

Install the following packages:

* build-essential
* git
* scons
* swig
* viewnior
* graphicsmagick

```console
$ sudo apt update
$ sudo apt install build-essential git scons swig viewnior graphicsmagick
```

Install the required Python packages:

* qrcode
* imagio
* pyserial
* requests
* Pillow
* rpi_ws281x


```console
$ sudo pip install qrcode[pil] imageio pyserial requests Pillow rpi_ws281x
```


## Install the GifyBox software

Install the software from the GitHub repository.

```console
$ cd
$ git clone https://github.com/informatik-mannheim/gify-box.git
```

The software client must be run as *root* to have access to the hardware, therefore you can use the starter script in the main directory of the project. Although, it is for the client only, we placed it there to make running the client as easy as possible.

Start the software on the box:

```
$ cd gify-box
$ ./launcher.sh
```


# Prevent Display Blanking

By default, the display will be turned off after a few moments. You won't notice this when the preview is open, because it overlays the blank screen somehow. But the replay of the GIF does not work. So we need to address and fix that.

Turing of the display blanking is done automatically by the [start script](../../launcher.sh). If you want to do it manually, enter the following two commands into the terminal:

```console
xset s off
xset -dpms
```
