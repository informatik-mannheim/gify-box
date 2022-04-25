#!/usr/bin/env python
"""
Main program for the Gify-Box.

This program is currently running with Python 2.

https://github.com/informatik-mannheim/gify-box
"""

import os
from time import sleep
from gpiozero import Button
import os, random, picamera, requests
from rpi_ws281x import *
from subprocess import Popen
import sys, select
import subprocess
import print_qr as at
import threading

### !! VAR DEFINITIONS !! ###

# Web server upload script. Change this to yout server's address
WEBSERVER_URL = 'http://gifybox.inno-space.de/upload.php'

# LED strip configuration. #1 is at button, #2 at the camera
LED_COUNT          = 8       # Number of LED pixels.
LED_PIN            = 18      # GPIO pin connected to the button pixels (must support PWM!).
LED_FREQ_HZ        = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA            = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS     = 50      # Set to 0 for darkest and 255 for brightest
LED_BRIGHTFAC      = 0.2     # factor of the default brightness
LED_INVERT         = False   # True to invert the signal (when using NPN transistor)

# GPIO pins according to BCM (http://pinout.xyz)
PINBTN = 23

# Picture configuration
PICTURE_COUNT   = 5
RESOLUTION      = (1280, 720)

# Picture wait delays
COMPLIMENT_WAIT = 0.8  # seconds
REPLAY_WAIT     = 24   # seconds
GOODBYE_WAIT    = 6    # seconds
STARTING_WAIT   = 1200/LED_COUNT    # if we wait that amount after each LED, the whole process takes 1 second
PHOTOSHOOT_WAIT = 360/LED_COUNT        # time between photos
GIF_DELAY       = 35 # How much time (1/100th seconds) between frames in the animated gif

# Color values (CAUTION: NOT RGB but GRB: Green, Red, Blue)
COLOR_OK                = Color(255, 0, 0)    #GREEN
COLOR_BLACK             = Color(0, 0, 0) # BLACK
COLOR_INITCOUNTDOWN1    = Color(150, 0, 0)
COLOR_INITCOUNTDOWN2    = Color(30, 0, 0)
COLOR_INITCOUNTDOWN3    = Color(10, 0, 0)
COLOR_INITCOUNTDOWN4    = Color(5, 0, 0)
COLOR_IMAGECOUNTDOWN    = Color(255, 255, 255)
COLOR_GIFGENERATION     = Color(0, 0, 255)
COLOR_GIFGENERATIONDARK = Color(0, 0, 120)
COLOR_REPLAY            = Color(0, 255, 0)

# Paths
PATH_FILEPATH      = os.path.dirname(os.path.abspath(__file__)) + "/"
PATH_DATAFILE      = PATH_FILEPATH + 'count.txt'
PATH_OUTPUT        = PATH_FILEPATH + 'output/'
PATH_OUTPUTROUND   = PATH_OUTPUT + 'round%06d/'
PATH_OUTPUTFILE    = PATH_OUTPUTROUND + 'frame%02d.jpg'
PATH_OUTPUTFILEGIF = PATH_OUTPUT + 'round%06d.gif'

# Branding logo overlay
OVERLAYIMAGE_SRC    = PATH_FILEPATH + 'media/logo_color.png'
OVERLAYIMAGE_OFFSET = (30, 10)

# Camera text annotations
CAMERA_TEXTCOLOR = picamera.Color('white')
CAMERA_TEXTBACKGROUNDCOLOR = picamera.Color('black')

CAMERA_TEXTVAL_START          = 'Get %d poses ready & press the button'%PICTURE_COUNT
CAMERA_TEXTVAL_STARTING1      = 'Taking Gif #%06d'
CAMERA_TEXTVAL_STARTING2      = 'Let`s go!'
CAMERA_TEXTVAL_STARTING3      = '3...'
CAMERA_TEXTVAL_STARTING4      = '2...'
CAMERA_TEXTVAL_STARTING5      = '1...'
CAMERA_TEXTVAL_PICINFORMATION = 'Taking picture #%d'
CAMERA_TEXTVAL_PROCESSING     = 'Stitching your photos together. Please wait :)'
CAMERA_TEXTVAL_PROCESSINGDONE = 'Almost there'
CAMERA_TEXTVAL_GOODBYE        = 'It was great having you here!'

# List of compliments displayed after each photo. Needs atleast as many entries as the picture count!!!
CAMERA_TEXTVAL_COMPLIMENTS = ['Looking good!', 'Oh yeah!', 'You rock!', 'Just like that!', 'Keep it up!', 'Yes!', 'Great!', 'Oh wow!', 'Perfect!', 'Nice!']

### !! DEFINITIONS DONE !! ###


### !! NEO PIXEL ANIMATIONS - SEE https://github.com/jgarff/rpi_ws281x !! ###

# Create NeoPixel object with appropriate configuration and intialize the library
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

def color_wipe(strip_to_use, color, wait_ms=20, reverse=False):
    """
    Perform a color wipe using the attached neopixels.
    """

    my_range = range(LED_COUNT) if not reverse else reversed(range(LED_COUNT))

    # wipe color: do a color wipe with this color
    for i in my_range:
        strip.setPixelColor(i, color)
        strip.show()
        if wait_ms > 0:
            sleep(wait_ms/1000.0)

# Show color instantaneous w/o any animation
def color_clear(strip_to_use, color):
    """
    Set the color without any delay.
    :param strip_to_use: the strip to be used
    :param color: the color to set
    """
    color_wipe(strip_to_use, color, wait_ms=0)


### !! NEO PIXEL ANIMATIONS DONE !! ###


### !! CAMERA FUNCTIONS !! ###

def camera_print_text(camera_to_use, text):
    """
    Show a text on the camera picture.

    :param camera_to_use: the camera to use
    :param text: the text to diplay
    """
    if text:
        camera_to_use.annotate_background = CAMERA_TEXTBACKGROUNDCOLOR
        camera_to_use.annotate_text_size = 64
        camera_to_use.annotate_text = ' ' + text + ' '
    else:
        camera_to_use.annotate_background = None
        camera_to_use.annotate_text = ''

### !! WEBSERVER AND QR CODE !! ###
def upload_and_print_qr(mround):
    """
    Function to be called in a separate thread. It uploads
    the pictures to the server and then prints the QR code
    using the attached printer. We put this together
    into one funtion because the upload is a prerequesite
    for the QR code. Therefore, it makes sense to have them
    together.

    :param mround: round counter - i.e. number of picture taken
    """
    images = [('image%d'%x, open(PATH_OUTPUTFILE%(mround,x), 'rb')) for x in range(PICTURE_COUNT)]
    r = requests.post(WEBSERVER_URL, files = images)
    with open("randomfile.txt","a") as o:
        o.write(str(r.status_code))

    print("upload finished with result code: %s" % str(r.status_code))

    if r.status_code == 200:
        filename = r.text
        print("printing user receipt with URL: %s" % str(r.text))
        at.print_qr_code(r.text)

def keystroke_watchdog():
    """
    Function to be called in a separate thread.

    This functions listens on a keystroke on stdin (due to the
    stdin buffering a keystroke plus enter) and then terminates
    the process the hard way. We use it to get out of the
    user interface of the camera.
    """
    print("Watchdog startet - waiting for keypress")
    # Allow quitting by pressing a key
    while True:
        a, b, c = select.select( [sys.stdin], [], [], 100)
        if (a != []):
           print(a)
           os._exit(0)

### !! BUSINESS LOGIC START !! ###

# start the camera
camera = picamera.PiCamera()
camera.resolution = RESOLUTION
#camera.rotation = 180

# turn off that red camera led
camera.led = False

# set camera annotation text color
camera.annotate_foreground = CAMERA_TEXTCOLOR

# start the camera preview and show the ok color w/ animation
camera.start_preview()
color_wipe(strip, COLOR_OK)
camera_print_text(camera, CAMERA_TEXTVAL_START)

# get the hardware button
button = Button(PINBTN)

# start the serial connection
#ser = serial.Serial(port='/dev/ttyACM0', baudrate=19200)

# get the data file and read the current round from there so we dont overwrite stuff
mround = 0
try:
    mfile = open(PATH_DATAFILE, 'r')
    mround = int(mfile.readline())
    mfile.close()
except:
    print("File content error")

# Start the keystroke watchdog thread
thread_keystroke = threading.Thread(target=keystroke_watchdog, args=())
thread_keystroke.start()

while True:

    # try to create a folder (don't abort if already there)
    try:
        os.mkdir(PATH_OUTPUTROUND%mround, 0o777)
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
        color_wipe(strip, COLOR_IMAGECOUNTDOWN, wait_ms=PHOTOSHOOT_WAIT, reverse=True)

        # clear the text and take a picture
        camera_print_text(camera, False)
        filepath = PATH_OUTPUTFILE%(mround,frame)
        camera.capture(filepath, use_video_port=True)

        # add branding and scale down the image using graphicsmagick
        graphicsmagick  = "gm composite "
        graphicsmagick += "-gravity SouthEast -geometry +" + str(OVERLAYIMAGE_OFFSET[0]) + "+" + str(OVERLAYIMAGE_OFFSET[1]) + " "    # bottom right with padding
        graphicsmagick += OVERLAYIMAGE_SRC + " " + filepath + " " + filepath # overlay image, source image, target image
        os.system(graphicsmagick)

        # clear the lights
        color_clear(strip, COLOR_BLACK)

        # show a compliment and sleep for a bit
        camera_print_text(camera, compliment_shuffle[frame])
        sleep(COMPLIMENT_WAIT)

        frame += 1

    # show gif generation lights
    camera_print_text(camera, CAMERA_TEXTVAL_PROCESSING)
    color_wipe(strip, COLOR_GIFGENERATION)

    # upload pictures to server in a separated thread
    # this takes the slow printing of the QR code of our plate
    upload_thread = threading.Thread(target=upload_and_print_qr, args=(mround,))
    upload_thread.start()

    # create the gif
    graphicsmagick = "gm convert -delay " + str(GIF_DELAY) + " " + PATH_OUTPUTROUND%mround + "*.jpg " + PATH_OUTPUTFILEGIF%mround
    os.system(graphicsmagick) #make the .gif

    # start the gif viewer
    command = ["viewnior", "--fullscreen", PATH_OUTPUTFILEGIF%mround]
    p = Popen(command)

    # display the text telling it is almost done, since we still need time to start the replay
    camera_print_text(camera, CAMERA_TEXTVAL_PROCESSINGDONE)

    # starting the gif viewer takes some time, so dont close the preview right away
    sleep(2)
    color_wipe(strip, COLOR_REPLAY)
    camera.stop_preview()

    # wait x seconds while showing the replay
    sleep(REPLAY_WAIT)

    # start the camera preview and close the gif viewer
    camera.start_preview()
    p.terminate()
    p.wait()

    # display the goodbye text
    camera_print_text(camera, CAMERA_TEXTVAL_GOODBYE)
    sleep(GOODBYE_WAIT)

    # show the ok color w/ animation
    color_wipe(strip, COLOR_OK)
    camera_print_text(camera, CAMERA_TEXTVAL_START)

    mround += 1

    # write the current round to the file
    f = open("count.txt", "w")
    f.write(str(mround))
    f.close()

    # Join upload thread
    upload_thread.join()


### !! BUSINESS LOGIC DONE !! ###
