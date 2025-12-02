import cv2
import numpy as np
import time

from picamera2 import Picamera2, Preview

# Screen Resolution
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 480

CAMERA_TEXTCOLOR = (255, 255, 255, 255)
CAMERA_TEXTBACKGROUNDCOLOR = (0, 0, 0, 255)
CAMERA_TEXTORIGIN = (50, 50)
CAMERA_TEXTFONT = cv2.FONT_HERSHEY_PLAIN
CAMERA_TEXTSCALE = 2
CAMERA_TEXTTHICKNESS = 2


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(1)

def camera_print_text(camera_to_use, text):
    if not text:
        text = ''
    overlay = np.zeros((PREVIEW_WIDTH, PREVIEW_HEIGHT, 4), dtype=np.uint8)
    text_size, _ = cv2.getTextSize(text, CAMERA_TEXTFONT, CAMERA_TEXTSCALE, CAMERA_TEXTTHICKNESS)
    text_w, text_h = text_size
    x, y = CAMERA_TEXTORIGIN
    cv2.rectangle(overlay, CAMERA_TEXTORIGIN, (x + text_w, y + text_h), CAMERA_TEXTBACKGROUNDCOLOR, -1)
    cv2.putText(overlay, text, CAMERA_TEXTORIGIN, CAMERA_TEXTFONT, CAMERA_TEXTSCALE, CAMERA_TEXTCOLOR, CAMERA_TEXTTHICKNESS)
    camera_to_use.set_overlay(overlay)

for time_left in range(3, 0, -1):
    text = f"Hallo Hallo {time_left} sec"
    camera_print_text(picam2, text)
    time.sleep(1)

camera_print_text(picam2, False)
time.sleep(2)
picam2.stop()