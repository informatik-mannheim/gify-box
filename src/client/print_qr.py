#!/usr/bin/python3

# We pulled out printing the actual QR code on the
# thermo printer into a separate file to allow us
# using Python 3 for this. As the main program is still
# written in Python 2, starting an external program
# is the easier approach.
# As soon as the main program is ported to Python 3,
# this could be merged into it.

import sys
import adafruit_thermal as at
from PIL import Image

# Get the text for the QR code from the command line
LOGO = "logo.png"

def print_qr_code(text):
    # read an image
    logo = Image.open(LOGO).convert('1', dither=Image.FLOYDSTEINBERG)

    printer = at.AdafruitThermal()
    printer.begin()
    printer.justify('C')

    printer.print_image(logo)
    printer.set_size('M')
    printer.println("proudly presents")
    printer.set_size('L')
    printer.println("Gify Box")

    printer.print_qr_code(text)
    printer.println(text)

if __name__ == "__main__":
    print_qr_code(sys.argv[1])