import cv2 
import numpy as np
import time
from find_device import isDevice, getAttributes
from find_text import findText
from helpers import showInWindow

def nothing(x):
    pass

def makeSafe(x: float) -> int:
    int = np.intp(x)
    return np.max([ 0, int ])

cap = cv2.VideoCapture('./data/test4.mp4')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 600, 600)

#defaults of 155 and 190 work with this example
cv2.createTrackbar("lower", "Trackbars", 150, 255, nothing)
cv2.createTrackbar("upper", "Trackbars", 255, 255, nothing)

#skips first 250 frames where back light is off
framenumber = 300
cap.set(cv2.CAP_PROP_POS_FRAMES, np.intp(framenumber))


while True:

    cap.set(cv2.CAP_PROP_POS_FRAMES, np.intp(framenumber))
    framenumber += 20

    _, frame = cap.read()

    frame2 = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    lower = cv2.getTrackbarPos("lower", "Trackbars")
    upper = cv2.getTrackbarPos("upper", "Trackbars")
 
    _, th2 = cv2.threshold(gray, lower, upper, 0)
    # contours, hierarchy = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    frame = cv2.drawContours(frame, contours, -1, (0,255,75), 2)

    for i in range(len(contours)):
        contour = contours[i]

        if isDevice(contour):

            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            w, h, cX, cY, rot = getAttributes(rect)
            x1 = makeSafe(cX - w/2)
            y1 = makeSafe(cY - h/2)
            x2 = makeSafe(cX + w/2)
            y2 = makeSafe(cY + h/2)

            #rotates the original image and crops so image only contains the screen (bounded by the contour)
            M = cv2.getRotationMatrix2D((cX, cY), rot, 1.0)
            height, width = frame.shape[:2]
            rotated = cv2.warpAffine(frame, M, (width, height))
            cropped = rotated[y1:y2, x1:x2]

            height, width = cropped.shape[:2]
            max = np.max([height, width])
            M2 = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1.0)
            rotated2 = cv2.warpAffine(cropped, M2, (max, max))

            parentArea = width * height            
            frame2 = findText(rotated2.copy(), lower, upper, parentArea, True)


    showInWindow('gg', th2, 700, 0)
    showInWindow('ggg', frame2, 700, 500)
    # showInWindow('gggg', frame, 0, 700)

    time.sleep(1)
    

    key = cv2.waitKey(1)
    if key == 27: # key 27 is "esc" key
        break

cap.release()
cv2.destroyAllWindows()