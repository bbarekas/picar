#!/usr/bin/python3
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)


while True:
    
    camera.capture(rawCapture, format="bgr")
    im = rawCapture.array

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(24, 24)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),1)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = im[y:y+h, x:x+w]

    cv2.imshow('video',im)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

picam2.stop()
cv2.destroyAllWindows()
