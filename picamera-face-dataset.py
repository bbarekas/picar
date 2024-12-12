#!/usr/bin/python3
import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform, controls 

face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

# For each person, enter one numeric face id
face_id = input('\n * Enter user id end press <return> ==> ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = -10

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
											 #transform=Transform(vflip=True))
picam2.configure(config)
#picam2.start_preview(Preview.QTGL)
picam2.start_preview(Preview.DRM)
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()

while(True):
    im = picam2.capture_array()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(24, 24)
    )
    
    cv2.imshow('image', im)
    for (x,y,w,h) in faces:
        cv2.rectangle(im, (x,y), (x+w,y+h), (255,0,0), 2)
        count += 1
        # Save the captured image into the datasets folder
        if (count >= 1):
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', im)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 101: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
picam2.stop()
cv2.destroyAllWindows()
