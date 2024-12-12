#!/usr/bin/python3
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls 

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
# "format": 'XRGB8888'
config = picam2.create_preview_configuration(main={"size": (640, 480)})
											 #transform=Transform(vflip=True))
picam2.configure(config)
#picam2.start_preview(Preview.QTGL)
picam2.start_preview(Preview.DRM)
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()

while True:
    im = picam2.capture_array()
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
