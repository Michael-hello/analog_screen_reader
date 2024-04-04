import numpy as np
import cv2
from helpers import getAttributes


#determins if a given contour is the LCD screen
def isDevice(contour) -> bool:

    area = cv2.contourArea(contour)

    #TO DO: this is rudimentary..
    if area > 100000:
        x, y, w, h = cv2.boundingRect(contour)
        ratio = np.max([w,h]) / np.min([w, h])

        #in a perfect world the ratio is approx 1.5      
        if ratio > 1.25 and ratio < 1.75:
            w, h, cX, cY, rot = getAttributes(cv2.minAreaRect(contour))
            #TO DO: better checking procedure
            if rot == 90:
                return False
            return True
    
    return False
     

