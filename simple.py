import cv2
import time

print("1")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

print("2")

time.sleep(2)

#
ret, frame = cap.read()

print("3")

print("Ret ", ret)
if ret:

    print("3.1")
    cv2.imwrite(image.jpg, frame)

print("4")

cap.release()


