#!/usr/bin/python3
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls
from buildhat import Motor, MotorPair, Hat
import numpy as np
import os
import time

# Moror functions
speed=10
# Stop.
def stop():
  pair.stop()

# Move forward.
def forward():
  hat.green_led(True)
  hat.orange_led(False)
  pair.run_for_degrees(90,speed,-speed)

# Move backward.
def backward():
  hat.green_led(False)
  hat.orange_led(True)
  pair.run_for_degrees(90,-speed,speed)

# Turn left.
def left():
  pair.run_for_degrees(90,speed,speed)

# Turn right.
def right():
  pair.run_for_degrees(90,-speed,-speed)



# Globals and settings
font = cv2.FONT_HERSHEY_SIMPLEX
# iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Bill', 'Kostas', 'Ilza', 'Z', 'W']
#
dist = 0
count = 0
found = False
n = 2
mm = np.zeros(n, dtype=int)


# Setup HAT motors
pair = MotorPair('A', 'B')
pair.set_default_speed(20)
hat = Hat()
print(hat.get())


# For each person, enter one numeric face id
face_id_str = input('\n * Enter user id to follow and press <return> ==> ')
face_id = int(face_id_str)
print(type(face_id))

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Load the previously trained model.
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Setup detector.
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# Initialize Pi camera
picam2 = Picamera2()
# "format": 'XRGB8888'
config = picam2.create_preview_configuration(main={"size": (640, 480)},
											 transform=Transform(vflip=True))
picam2.configure(config)
#picam2.start_preview(Preview.QTGL)
picam2.start_preview(Preview.DRM)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()

print("Looking for face: {0}".format(face_id))
# 
while True:
    found = False

    im = picam2.capture_array()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(24, 24),
    )

    # Process faces.
    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        if (id == face_id) and (confidence < 100) :
            print("Found: {0} p:{1}".format(id, confidence))
            found = True
            mm[count%n] = w
            count = count + 1
            

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = "{0} {1}x{2}".format(names[id], w, h)
            confidence = "  {0}%".format(round(100 - confidence))
            #time.sleep(1)
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(im, str(id), (x + 5, y - 5), font, 0.7, (255, 255, 255), 2)
        cv2.putText(im, str(confidence), (x + 5, y + h - 5), font, 0.4, (255, 255, 0), 1)


    dist = mm.mean()
    if found:
        if dist < 250-20:
            print("Forward ... {0}".format(dist))
            forward()
        elif dist > 250+20:
            print("Backward ... {0}".format(dist))
            backward()
        else:
            # Stay still
            print("Still ... {0}".format(dist))
            stop()

    else:
        # Reset
        print("Stop ... {0}".format(dist))
        mm = np.zeros(n, dtype=int)
        count = 0
        stop()

    # Display the image and rectangle. 
    cv2.imshow('camera', im)

    k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
picam2.stop()
cv2.destroyAllWindows()
