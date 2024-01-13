#!/usr/bin/env python3
import cv2
import io
import time
from picamera2 import Picamera2
import numpy as np
from pathlib import Path

MIN_CONTOUR_SIZE = 1500
GREEN_RGB = (0, 255, 0)
COUNT = 250
IMAGES_DIR = Path("/home/pi/bird_tracker/static/images")

def get_image(cam):
    buff = io.BytesIO()
    cam.capture_file(buff, format='jpeg')
    image = cv2.imdecode(np.frombuffer(buff.getbuffer(), np.uint8), -1)
    return image


def validate_detection(detection) -> bool:
    if cv2.contourArea(detection) < MIN_CONTOUR_SIZE:
        return False
    return True


camera = Picamera2()
preview_config = camera.create_still_configuration(main={"size": (1280, 720)})
camera.configure(preview_config)

camera.start()
time.sleep(1)

times = []

shift = len([_ for _ in IMAGES_DIR.iterdir()])
counter = shift + 1

print(f"Start processing from {counter}")
ss = time.time()
while ((COUNT + shift) >= counter):

    start = time.time()

    img1 = get_image(camera)
    img2 = get_image(camera)

    duration = time.time() - start
    # print(f'Take photo {duration}')
    times.append(duration)

    start = time.time()
    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    finish = time.time()
    # print(f'Processing photo {finish-start}')

    contours = [c for c in contours if validate_detection(c)]
    if contours:
        counter += 1
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img2, (x, y), (x + w, y + h), GREEN_RGB, 2)

        name = f'motion{counter}.jpg'
        path = IMAGES_DIR / name
        cv2.imwrite(str(path), img2)
        print(f'Save {path} with {len(contours)} detections')
    # print('=' * 70)

ff = time.time()
camera.stop()

print(f'Total pipline: {ff - ss}')
print(f'AVG photo: {sum(times) / len(times)}')
