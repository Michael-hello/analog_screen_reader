import cv2 
import numpy as np
import time
import pytesseract
from define_text import defineText

def getTextTesseract(image):       

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    resized = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    config = '--psm 6' #13 tessedit_char_whitelist=0123456789'# --oem 3 -c tessedit_char_whitelist=0123456789'
    data = pytesseract.image_to_string(resized, lang='eng', config=config)

    print('text: ', data)



#parent area is area of the cropped image containing the screen
def findText(cropped, lower, upper, parentArea, toBlack = False):

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    _, th2 = cv2.threshold(gray, lower, upper, 0)
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    black_img = np.array(cropped.copy())
    black_img[:, :, :3] = 0

    image = cropped
    if toBlack: image = black_img
    
    filteredContours = []

    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])

        #below limits work well to isolate the numerical values
        if area > 0 and parentArea > 0:

            # contour = cv2.approxPolyDP(contours[i])
            areaRatio = parentArea / area
            x, y, w, h = cv2.boundingRect(contours[i])
            ratio = np.max([w,h]) / np.min([w, h])

            if areaRatio < 1000 and areaRatio > 100 and ratio > 2.2:
                contours2 = [ cv2.approxPolyDP(contours[i], 10, True) ]
                image = cv2.drawContours(image, contours2, 0, (255, 255, 255), thickness=cv2.FILLED)
                filteredContours.append(contours[i])              
    
    defineText(filteredContours)


    return image