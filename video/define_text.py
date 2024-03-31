import cv2 
import numpy as np

class Slice:

    def __init__(self, isVert, contour):
        self.isVert = isVert
        self.contour = contour


class Digit:

    def __init__(self, slice):
        self.slices = [ slice ]

#pos == 0 for x, pos == 1 for y
def getVals(contour, pos: int):  

    if len(contour) == 0:
        return None
    
    x = []

    for i in range(len(contour)):
        vert = contour[i]
        x.append(vert[0][pos])

    return x


def digitToText(digit: Digit) -> int:

    slices = digit.slices
    count = len(slices)
    vCount = filter(lambda x: x.isVert == True, slices)
    hCount = filter(lambda x: x.isVert == False, slices)

    if count == 2:
        return 1   
     
    if count == 7:
        return 8  
      
    if count == 4:
        return 4
    
    if count == 3: 
        return 7
    
    if count == 6 and vCount == 3:
        return 6
    
    if count == 6 and hCount == 2:
        return 0
    
    if count == 5 and vCount == 3:
        return 9
    
    if count == 5:
        #TO DO: implement logic for 2 3 and 5
        return #2 3 5


#contours is an array of slices defining different digits
def defineText(contours):

    digits = []

    #each contour defines a slice of 1 or more digits
    for i in range(len(contours)):
        contour = contours[i]

        contour2 = cv2.approxPolyDP(contours[i], 10, True)
        x, y, w, h = cv2.boundingRect(contour2)

        xVals = getVals(contour2, 0)
        yVals = getVals(contour2, 1)

        xMax = np.max(xVals)
        xMin = np.min(xVals)
        yMax = np.max(yVals)
        yMin = np.min(yVals)

        # xDiff = xMax - xMin
        # yDiff = yMax - yMin

        isVert = h > 1.5 * w

        slice = Slice(isVert, contour2)

        if len(digits) == 0:
            digits.append(Digit(slice))   
        
        #TO DO: determine which digit the slice belongs to



    
    #area = cv2.contourArea(contour) 
    return