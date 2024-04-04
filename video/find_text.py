import cv2 
import numpy as np
import time
import pytesseract
from define_text import defineText
from helpers import getAttributes

def getTextTesseract(image):       

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    resized = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    config = '--psm 6' #13 tessedit_char_whitelist=0123456789'# --oem 3 -c tessedit_char_whitelist=0123456789'
    data = pytesseract.image_to_string(resized, lang='eng', config=config)

    print('text: ', data)


def getParams(contour):

    if len(contour) < 2:
        return None
    
    getX = lambda contour: contour[0][0]
    getY = lambda contour: contour[0][1]

    maxX: float = getX(contour[0])
    minY: float = getY(contour[0])

    for i in range(len(contour)):
        x = getX(contour[i])
        y = getY(contour[i])
        if x > maxX: maxX = x
        if y < minY: minY = y

    return maxX, minY


# #if contour is too close to top or side of screen: invalid
def validateContour(contour, screen_contour) -> bool:

    tollarance = 20
    maxX_screen, minY_screen = getParams(screen_contour)
    maxX, minY = getParams(contour)

    if np.abs(maxX_screen - maxX) < tollarance:
        return False    

    return True


#isolates contours that define the numerical text
def findText(cropped, lower, upper, adaptive = False, lab = False, limit=2.0, grid=8):

    # cropped = cv2.resize(cropped.copy(), (0,0), fx=2, fy=2) 
    gray = cv2.cvtColor(cropped.copy(), cv2.COLOR_BGR2GRAY)
    _, th2 = cv2.threshold(gray, lower, upper, cv2.THRESH_BINARY)  

    #see: https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    if lab:

        lab_img = cv2.cvtColor(cropped.copy(), cv2.COLOR_BGR2LAB)
        l_channel, a, b = cv2.split(lab_img)    
        clahe = cv2.createCLAHE(clipLimit=limit, tileGridSize=(grid,grid))
        cl = clahe.apply(l_channel)
        # merge the CLAHE enhanced L-channel with the a and b channel
        limg = cv2.merge((cl,a,b))
        img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, th2 = cv2.threshold(gray2, lower-10, upper, cv2.THRESH_BINARY)
        

    if adaptive:
        th2 = cv2.adaptiveThreshold(gray, 255 ,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, -2)
 
     
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours) == 0:
        return

    #allows contours to be drawn
    image = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)       
    filteredContours = []  

    largest_contour = contours[0]
    largest_area = cv2.contourArea(contours[0])
    
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])

        if area > largest_area:
            largest_area = area
            largest_contour = contours[i]

    image = cv2.drawContours(image, [ largest_contour ], 0, (0, 255, 0), thickness=2) #cv2.FILLED)

    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])

        #below limits work well to isolate the numerical values
        if area > 500:

            areaRatio = largest_area / area
            x, y, w, h = cv2.boundingRect(contours[i])
            ratio = np.max([w,h]) / np.min([w, h])

            if areaRatio < 500 and areaRatio > 5 and ratio > 1.25:

                contours2 = cv2.approxPolyDP(contours[i], 2, True)
                
                if validateContour(contours2, largest_contour) == False:
                    continue

                image = cv2.drawContours(image, [ contours2 ], 0, (0, 0, 255), thickness=2) #cv2.FILLED)
                filteredContours.append(contours2)              
    
    #defines the text based on contours
    digitised_val = defineText(filteredContours)


    return image, digitised_val


