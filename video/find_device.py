import numpy as np
import cv2

#below params describe the output of minAreaRect  https://stackoverflow.com/questions/57967420/what-is-the-output-of-minarearectcontours
#center    The rectangle mass center.
#size      Width and height of the rectangle.
#angle     The rotation angle in a clockwise direction. When the angle is 0, 90, 180, 270 etc., the rectangle becomes an up-right rectangle.
def getAttributes(box):
    w = box[1][0]
    h = box[1][1]
    cX = box[0][0]
    cY  = box[0][1]
    rot = box[2]
    return w, h, cX, cY, rot

def isDevice(contour) -> bool:

    area = cv2.contourArea(contour)

    if area > 100000:
        x, y, w, h = cv2.boundingRect(contour)
        ratio = np.max([w,h]) / np.min([w, h])

        #in a perfect world the ratio is approx 1.5      
        if ratio > 1.25 and ratio < 1.75:
            w, h, cX, cY, rot = getAttributes(cv2.minAreaRect(contour))
            print(ratio, area, w , h)
            return True
    
    return False
     

