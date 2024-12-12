import numpy as np
import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(cv2.__version__)


print_hi('Ok Computer')


# initialize the camera and grab a reference to the raw camera capture
#cap = PiCamera()
#rawCapture = PiRGBArray(cap)

# allow the camera to warmup
#time.sleep(0.1)


#cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
#cap.set(3, 640)  # set Width
#cap.set(4, 480)  # set Height

#while (True):
#    ret, frame = cap.read()
#    frame = cv2.flip(frame, -1)  # Flip camera vertically
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#    cv2.imshow('frame', frame)
    #cv2.imshow('gray', gray)

#    k = cv2.waitKey(30) & 0xff
##    if k == 27:  # press 'ESC' to quit
#        break

#cap.release()
#cv2.destroyAllWindows()
