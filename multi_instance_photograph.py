#!/usr/bin/env python
from time import sleep
from gpiozero import Button
import os, random, picamera, requests
from neopixel import *

### !! VAR DEFINITIONS !! ###


# LED strip configuration. #1 is at button, #2 at the camera
LED_COUNT1     	= 24      # Number of LED pixels.
LED_COUNT2     	= 16      # Number of LED pixels.
LED_PIN       	= 18      # GPIO pin connected to the button pixels (must support PWM!).
LED_FREQ_HZ    	= 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        	= 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS	= 50      # Set to 0 for darkest and 255 for brightest
LED_BRIGHTFAC 	= 0.2     # factor of the default brightness
LED_INVERT     	= False   # True to invert the signal (when using NPN transistor)

# GPIO pins according to BCM (http://pinout.xyz)
PINBTN = 23



# Picture configuration
PICTURE_COUNT   = 5
RESOLUTION 		= (1280, 720)



# Picture wait delays
COMPLIMENT_WAIT = 0.8 # seconds
GOODBYE_WAIT    = 3 # seconds
STARTING_WAIT	= 2500/LED_COUNT1	# if we wait that amount after each LED, the whole process takes 1 second
PHOTOSHOOT_WAIT	= 500/LED_COUNT2	# time between photos



# Color values (CAUTION: NOT RGB but GRB: Green, Red, Blue)
COLOR_OK = Color(255, 0, 0)	#GREEN
COLOR_BLACK = Color(0, 0, 0) # BLACK
COLOR_INITCOUNTDOWN1 = Color(150, 0, 0)
COLOR_INITCOUNTDOWN2 = Color(30, 0, 0)
COLOR_INITCOUNTDOWN3 = Color(10, 0, 0)
COLOR_INITCOUNTDOWN4 = Color(5, 0, 0)
COLOR_IMAGECOUNTDOWN = Color(35, 15, 105)
COLOR_UPLOAD = Color(255, 255, 255)



# Paths
PATH_FILEPATH = '/home/pi/photobooth/'
PATH_DATAFILE = PATH_FILEPATH + 'count.txt'
PATH_OUTPUT = PATH_FILEPATH + 'output/'
PATH_OUTPUTROUND = PATH_OUTPUT + 'round%06d/'
PATH_OUTPUTFILE = PATH_OUTPUTROUND + 'frame%02d.jpg'



# Camera text annotations
CAMERA_TEXTCOLOR = picamera.Color('white')
CAMERA_TEXTBACKGROUNDCOLOR = picamera.Color('black')

CAMERA_TEXTVAL_START = 'Get %d poses ready & press the button to start'%PICTURE_COUNT
CAMERA_TEXTVAL_STARTING1 = 'Photobooth is starting. Session #%06d'
CAMERA_TEXTVAL_STARTING2 = 'It will take %d pictures'%PICTURE_COUNT
CAMERA_TEXTVAL_STARTING3 = 'The camera LED circle will fill up'
CAMERA_TEXTVAL_STARTING4 = 'When it\'s full, a photo is taken'
CAMERA_TEXTVAL_STARTING5 = 'Get ready! We are launching.'
CAMERA_TEXTVAL_PICINFORMATION = 'Taking picture #%d'
CAMERA_TEXTVAL_GOODBYE = 'Check out your GIF on the other display!'

# List of compliments displayed after each photo. Needs atleast as many entries as the picture count!!!
CAMERA_TEXTVAL_COMPLIMENTS = ['Awesome!', 'Looking good!', 'Oh yeah!', 'You rock!', 'Just like that!', 'Keep it up!', 'Yes!', 'Great!', 'Oh wow!', 'Perfect!', 'Nice!']


# webserver data
WEBSERVER_URL = 'http://37.61.204.167/photobooth/upload.php'

### !! DEFINITIONS DONE !! ###



### !! NEO PIXEL ANIMATIONS - SEE https://github.com/jgarff/rpi_ws281x !! ###

# Create NeoPixel object with appropriate configuration and intialize the library
strip = Adafruit_NeoPixel(LED_COUNT1+LED_COUNT2, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()



# Define functions which animate LEDs in various ways.
# Asuming the default call is for the button LEDs
def color_wipe(strip, color, wait_ms=20, is_button_with_leds=True):
	add = LED_COUNT1 if is_button_with_leds else 0	# offset the leds for the camera leds
	count = LED_COUNT2 if is_button_with_leds else LED_COUNT1	# offset the leds for the camera leds

	# wipe color: do a radiant animation with this color
	for i in range(count):
		strip.setPixelColor(i+add, color)
		strip.show()
		if wait_ms > 0:
			sleep(wait_ms/1000.0)

# Show color instantaneous w/o any animation
def color_clear(strip, color, is_button_with_leds=True):
	color_wipe(strip, color, wait_ms=0, is_button_with_leds=is_button_with_leds)


### !! NEO PIXEL ANIMATIONS DONE !! ###


### !! CAMERA FUNCTIONS !! ###

def camera_print_text(camera, text):
	if text:
		camera.annotate_background = CAMERA_TEXTBACKGROUNDCOLOR
		camera.annotate_text = ' '+text+' '
	else:
		camera.annotate_background = None
		camera.annotate_text = ''


### !! BUSINESS LOGIC START !! ###

# start the camera
camera = picamera.PiCamera()
camera.resolution = RESOLUTION

# turn off that red camera led
camera.led = False

# set camera annotation text color
camera.annotate_foreground = CAMERA_TEXTCOLOR

# start the camera preview and show the ok color w/ animation
camera.start_preview()
color_wipe(strip, COLOR_OK)
color_clear(strip, COLOR_BLACK, is_button_with_leds=False)
camera_print_text(camera, CAMERA_TEXTVAL_START)

# get the hardware button
button = Button(PINBTN)

# get the data file and read the current round from there so we dont overwrite stuff
mround = 0
try:
        mfile = open(PATH_DATAFILE, 'r')
        mround = int(mfile.readline())
        mfile.close()
except:
        print("File content error")
        


while True:

	# try to create a folder (don't abort if already there)
	try:
		os.mkdir(PATH_OUTPUTROUND%mround, 0777)
	except OSError:
		print("dir already there")

	# wait for the button press
	button.wait_for_press()
	camera_print_text(camera, CAMERA_TEXTVAL_STARTING1%mround)

	# do start animation
	color_wipe(strip, COLOR_INITCOUNTDOWN1, wait_ms=STARTING_WAIT)
	camera_print_text(camera, CAMERA_TEXTVAL_STARTING2)
	color_wipe(strip, COLOR_INITCOUNTDOWN2, wait_ms=STARTING_WAIT)
	camera_print_text(camera, CAMERA_TEXTVAL_STARTING3)
	color_wipe(strip, COLOR_INITCOUNTDOWN3, wait_ms=STARTING_WAIT)
	camera_print_text(camera, CAMERA_TEXTVAL_STARTING4)
	color_wipe(strip, COLOR_INITCOUNTDOWN4, wait_ms=STARTING_WAIT)
	camera_print_text(camera, CAMERA_TEXTVAL_STARTING5)
	color_wipe(strip, COLOR_BLACK, wait_ms=STARTING_WAIT)

	# get x random unique compliments
	compliment_shuffle = random.sample(CAMERA_TEXTVAL_COMPLIMENTS, PICTURE_COUNT)

	# frame animate
	frame = 0

	# loop through the pictures
	while frame < PICTURE_COUNT:
		# show photo number and start light animation
		camera_print_text(camera, CAMERA_TEXTVAL_PICINFORMATION%(frame+1))
		color_wipe(strip, COLOR_IMAGECOUNTDOWN, wait_ms=PHOTOSHOOT_WAIT, is_button_with_leds=False)

		# clear the text and take a picture
		camera_print_text(camera, False)
		filepath = PATH_OUTPUTFILE%(mround,frame)
		camera.capture(filepath, use_video_port=True)

		# clear the lights
		color_clear(strip, COLOR_BLACK, is_button_with_leds=False)

		# show a compliment and sleep for a bit
		camera_print_text(camera, compliment_shuffle[frame])
		sleep(COMPLIMENT_WAIT)

		frame += 1

	# display the goodbye text
	camera_print_text(camera, CAMERA_TEXTVAL_GOODBYE)
	color_wipe(strip, COLOR_UPLOAD)

	# upload pictures to server
	images = [('images', ('img%d.png'%x, PATH_OUTPUTFILE%(mround,x), 'image/png')) for x in range(PICTURE_COUNT)]
	print images
	r = requests.post(WEBSERVER_URL, files=images)
	print r.text

	# sleep some more
	sleep(GOODBYE_WAIT)

	# show the ok color w/ animation
	color_wipe(strip, COLOR_OK)
	camera_print_text(camera, CAMERA_TEXTVAL_START)

	mround += 1

	# write the current round to the file
	f = open(PATH_DATAFILE, "w")
	f.write(str(mround))
	f.close()

### !! BUSINESS LOGIC DONE !! ###
