import cv2 
import numpy as np
import time
from find_device import isDevice, getAttributes
from find_text import findText
from helpers import showInWindow, makeSafe, saveImage, deleteAllFiles, formatValue

def nothing(x):
    pass

deleteAllFiles('./results')

cap = cv2.VideoCapture('./data/test4.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 600, 600)

#defaults of 150 and 255 work well with this example
cv2.createTrackbar("lower", "Trackbars", 150, 255, nothing)
cv2.createTrackbar("upper", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("limit", "Trackbars", 2, 100, nothing)
cv2.createTrackbar("grid", "Trackbars", 14, 30, nothing)

#skips first 200frames where back light is off
framenumber = 200 #525
cap.set(cv2.CAP_PROP_POS_FRAMES, np.intp(framenumber))
validValues = 0

while True:

    ret, frame = cap.read()
    framenumber += 1

    if framenumber >= total_frames:
        break
    
    frame2 = frame.copy()
    frame3 = frame.copy()
    frame4 = frame.copy()
    digitised_val = None

    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    
    lower = cv2.getTrackbarPos("lower", "Trackbars")
    upper = cv2.getTrackbarPos("upper", "Trackbars")
 
    _, th2 = cv2.threshold(gray.copy(), 150, 255, 0)
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

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

            #applies a 90 degree rotation so image is horizontal
            height, width = cropped.shape[:2]
            max = np.max([height, width])
            M2 = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1.0)
            rotated2 = cv2.warpAffine(cropped, M2, (max, max))
            
            frame = rotated2.copy()         
            limit = cv2.getTrackbarPos("limit", "Trackbars")
            grid = np.intp(cv2.getTrackbarPos("grid", "Trackbars"))

            frame4, digitised_val = findText(rotated2.copy(), lower, upper, False, True, limit, grid)



    # showInWindow('lab', frame4, 1300, 0)
    # time.sleep(0.2) 

    if digitised_val != None:
        validValues += 1
    
    label = str(framenumber) + '_' + formatValue(digitised_val)
    image = cv2.putText(frame4, label, (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, 2) 
    saveImage(image, label) 

    key = cv2.waitKey(1)
    if key == 27: # key 27 is "esc" key
        break

print('VALID VALUES: ', str(validValues))
cap.release()
cv2.destroyAllWindows()