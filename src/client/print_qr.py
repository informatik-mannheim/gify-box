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
LOGO = "media/logo_bw.png"

def print_qr_code(text):
    # read an image
    logo = Image.open(LOGO).convert('1', dither=Image.Dither.FLOYDSTEINBERG)

    printer = at.AdafruitThermal()
    printer.begin()
    printer.justify('C')

    printer.println()
    printer.print_image(logo)
    printer.set_size('S')
    printer.println("https://inno-space.de")
    printer.set_size('M')
    printer.println("proudly presents")
    printer.set_size('L')
    printer.println("Gify Box")
    printer.println()
    printer.set_size('S')
    printer.println("Download your picture here:")
    printer.print_qr_code(text)
    printer.println(text)
    printer.println()
    printer.println()
    printer.println()
    printer.println()

if __name__ == "__main__":
    print_qr_code(sys.argv[1])
