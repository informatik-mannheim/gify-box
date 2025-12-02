# GifyBox

RaspberryPi Photobooth software written in Python using [Adafruit Neopixels](https://www.adafruit.com/category/168) and a [Raspberry Pi Camera](https://www.raspberrypi.org/help/camera-module-setup/).


# What is this?

This is a software and a hardware implementation for a photobooth, where people can create stop motion gifs. For this, people can sit in front of a camera and start the capture process by pressing a hardware button. Then the software takes a predefined amount of pictures and generates a GIF. Afterwards it plays the GIF and uploads it to an online service. To guide the user, there are also visualizations using a display and Neopixel LEDs.

![title image](media/in-action.jpg)

Check the flyer in [english](/media/flyer.pdf) and [german](/media/flyer-de.pdf) for additional information on the Software and box.

# What do you need?

## Full version

You need a **Raspberry Pi**. We would recommend a **RPi 4 Rev. B**, since the older version are slower and the GIF generation takes longer. Therefore, the user experience might is worse. Also you need the mandatory hardware for the Raspberry Pi: an **USB-C power adapter with 5V and at least 2A** & a **microSD card with at least 16GB** memory. Additionally, a mouse and keyboard for debugging. And a LAN cable if you don't use WIFI.

To print the receipts you need:

* an **[Adafruit Mini Thermal Receipt Printer](https://www.adafruit.com/product/597)**
* a **cable** to connect the Thermal Printer to the Raspberry Pi

Additional Hardware:

* a **display with HDMI** and an HDMI cable connected to the RPi. You can use an old **laptop display with LVDS** (most displays use LVDS, but you should make sure, yours does as well) and a **LVDS converter board**
* a **[Raspberry Pi camera](https://www.raspberrypi.org/help/camera-module-setup/)**
* some **hardware buttons and cables**
* two **[Neopixel strips with 8 pixels](https://www.adafruit.com/products/1460)** (you can use any other amount or length)

Additionally, you need a **web server** for the website supporting PHP and ImageMagick.


## Modifications

You can modify the setup to satisfy your needs.

You can get rid of the printer. In this case you should also get rid of the serial code inside the python script.

You can get rid of the web server and only save the images locally. For this you should remove the part from the python script.

You can remove the logos from the images by removing the *gm composite* command from the python script.

You can modify the text by modifying the `CAMERA_TEXTVAL_*` values. You can modify the timings by modyfying the `*_WAIT` values. You can modify the color strip colors by modifying the `COLOR_*` values. See the [main Python file](src/client/single_instance.py) of the client for details.

# Hardware setup

Connect the hardware from above to the Raspberry Pi. Plug in the display and the input devices. Connect the camera to the camera port on the Raspberry Pi. Connect the button and Neopixels according to the Fritzing layout below. Connect the printer to the RaspberryPI according to the layout. The printer must be powered with an external power supply!

![hardware](media/sketch.svg)

# Client-Installation

Get your Raspberry Pi working with Raspbian following [the official tutorials](https://www.raspberrypi.org/help/quick-start-guide/).

Follow the [client installation instructions](src/client/README.md) in the client folder.

# Server-Installation

The software uses PHP as the underlying platform and a Linux server.

Follow the [server installation instructions](src/server/README.md) in the client folder.
