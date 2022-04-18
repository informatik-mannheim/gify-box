# Installation

## Install additional packages

Install the following packages: build-essential git scons swig viewnior graphicsmagick

```console
$ sudo apt install build-essential git scons swig viewnior graphicsmagick cmake
``` 

Install the required Python packages:

```console
$ sudo pip install qrcode[pil] imageio pyserial requests Pillow rpi_ws281x
``` 

## Build and install the Neopixel Library

```console
$ git clone https://github.com/jgarff/rpi_ws281x.git
$ cd rpi_ws281x/
$ scons
$ mkdir build
$ cd build
$ cmake -D BUILD_SHARED=OFF -D BUILD_TEST=ON ..
$ cmake --build .
$ sudo make install
```

## Install the GifyBox

```console
$ cd
$ git clone https://github.com/informatik-mannheim/gify-box.git
$ cd gify-box/src/client/
$ ./launcher.sh
```



