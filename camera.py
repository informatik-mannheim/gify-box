#!/usr/bin/env python
from picamera import PiCamera
from time import sleep
from gpiozero import Button
import os
from neopixel import *
from subprocess import Popen

### !! VAR DEFINITIONS !! ###

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor l

# Picture configuration
PICTURE_COUNT   = 5
SLEEPBETWEEN    = 1 # seconds
SLEEPAFTER      = 20 # seconds
ANIMATION_WAIT	= 1000/LED_COUNT	# if we wait that amount after each LED, the whole process takes 1 second
RESOLUTION 		= (1280, 720)

# How much time between frames in the animated gif
GIF_DELAY = 25 

# GPIO pins according to BCM (http://pinout.xyz)
PINBTN = 23
PINLED = 24

# color values (CAUTION: NOT RGB but GRB: Green, Red, Blue)
COLOR_OK = Color(255, 0, 0)	#GREEN
COLOR_BLACK = Color(0, 0, 0) # BLACK
COLOR_INITCOUNTDOWN1 = Color(255, 0, 0)
COLOR_INITCOUNTDOWN2 = Color(255, 63, 127)
COLOR_IMAGECOUNTDOWN = Color(127, 255, 127)
COLOR_GIFGENERATION = Color(0, 0, 255)
COLOR_REPLAY = Color(255, 255, 255)

# Paths
PATH_FILEPATH = '/home/pi/photobooth/'
PATH_OUTPUT = PATH_FILEPATH + 'output/'
PATH_OUTPUTROUND = PATH_OUTPUT + 'round%06d/'
PATH_OUTPUTFILE = PATH_OUTPUTROUND + 'frame%02d.jpg'
PATH_OUTPUTFILEGIF = PATH_OUTPUT + 'round%06d.gif'

### !! DEFINITIONS DONE !! ###



### !! NEO PIXEL ANIMATIONS - SEE https://github.com/jgarff/rpi_ws281x !! ###

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# Intialize the library (must be called once before other functions).
strip.begin()


# Define functions which animate LEDs in various ways.
def colorClear(strip, color):
	# show color on all pixels
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=20):
	# wipe color: do a radiant animation with this color
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		sleep(wait_ms/1000.0)

def wheel(pos):
	# get a color for a position
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	# rainbow fade animation
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		if not animate:
			return
		strip.show()
		sleep(wait_ms/1000.0)

### !! NEO PIXEL ANIMATIONS DONE !! ###



### !! BUSINESS LOGIC START !! ###

# start the camera
camera = PiCamera()
camera.resolution = RESOLUTION

# start the camera preview and show the ok color w/ animation
camera.start_preview()
colorWipe(strip, COLOR_OK)

# get the hardware button
button = Button(PINBTN)

# round increment
mround = 0

while True:

	# try to create a folder (don't abort if already there)
	try:
		os.mkdir(PATH_OUTPUTROUND%mround, 0777)
	except OSError:
		print "dir already there"

	# wait for the button press
	button.wait_for_press()

	# do start animation
	colorWipe(strip, COLOR_INITCOUNTDOWN1, wait_ms=ANIMATION_WAIT)
	colorWipe(strip, COLOR_BLACK, wait_ms=ANIMATION_WAIT)
	colorWipe(strip, COLOR_INITCOUNTDOWN2, wait_ms=ANIMATION_WAIT)
	colorWipe(strip, COLOR_BLACK, wait_ms=ANIMATION_WAIT)

	# frame animate
	frame = 0

	# loop through the pictures
	while frame < PICTURE_COUNT:
		# start light animation
		colorWipe(strip, COLOR_IMAGECOUNTDOWN, wait_ms=ANIMATION_WAIT*2)

		# take a picture
		camera.capture(PATH_OUTPUTFILE%(mround,frame), use_video_port=True)

		# clear the lights
		colorClear(strip, COLOR_BLACK)

		frame += 1

	# show git generation lights
	colorWipe(strip, COLOR_GIFGENERATION)

	# create the gif
	graphicsmagick = "gm convert -delay " + str(GIF_DELAY) + " " + PATH_OUTPUTROUND%mround + "*.jpg " + PATH_OUTPUTFILEGIF%mround 
	os.system(graphicsmagick) #make the .gif

	# start the gif viewer
	command = ["viewnior", "--fullscreen", PATH_OUTPUTFILEGIF%mround]
	p = Popen(command)

	# starting the gif viewer takes some time, so dont close the preview right away
	sleep(2)
	colorWipe(strip, COLOR_REPLAY)
	camera.stop_preview()

	sleep(SLEEPAFTER)


	# start the camera preview and show the ok color w/ animation
	camera.start_preview()
	colorWipe(strip, COLOR_OK)

	# close the gif viewer
	p.terminate()
	p.wait()

### !! BUSINESS LOGIC DONE !! ###