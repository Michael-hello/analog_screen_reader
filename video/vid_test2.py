import cv2 
import numpy as np
import time
from find_device import isDevice, getAttributes
from find_text import findText

def nothing(x):
    pass

cap = cv2.VideoCapture('./data/test4.mp4')

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 600, 600)

#defaults of 155 and 190 work with this example
cv2.createTrackbar("lower", "Trackbars", 155, 255, nothing)
cv2.createTrackbar("upper", "Trackbars", 190, 255, nothing)

#skips first 250 frames where back light is off
cap.set(cv2.CAP_PROP_POS_FRAMES, 250)


while True:

    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    lower = cv2.getTrackbarPos("lower", "Trackbars")
    upper = cv2.getTrackbarPos("upper", "Trackbars")
 
    _, th2 = cv2.threshold(gray, lower, upper, 0)
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        contour = contours[i]

        if isDevice(contour):

            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            w, h, cX, cY, rot = getAttributes(rect)
            x1 = np.intp(cX - w/2)
            y1 = np.intp(cY - h/2)
            x2 = np.intp(cX + w/2)
            y2 = np.intp(cY + h/2)

            M = cv2.getRotationMatrix2D((cX, cY), rot, 1.0)
            height, width = frame.shape[:2]
            rotated = cv2.warpAffine(frame, M, (width, height))
            cropped = rotated[y1:y2, x1:x2]

            frame = findText(cropped, lower, upper)
    
            # frame = cv2.drawContours(cropped, contours, i, (50, 250, 50), 2)
            # frame = cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)


    cv2.imshow("frame", cv2.resize(frame, (0,0), fx=0.5, fy=0.5))
    cv2.imshow("mask", cv2.resize(th2, (0,0), fx=0.5, fy=0.5) )

    # time.sleep(10)

    key = cv2.waitKey(1)
    if key == 27: # key 27 is "esc" key
        break

cap.release()
cv2.destroyAllWindows()