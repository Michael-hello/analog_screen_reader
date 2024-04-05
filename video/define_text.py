import cv2 
import numpy as np
from digits import Digit, Slice
from digit_2_val import digitToText

#pos == 0 for x, pos == 1 for y
def getVals(contour, pos: int):  

    if len(contour) == 0:
        return None
    
    x = []

    for i in range(len(contour)):
        vert = contour[i]
        x.append(vert[0][pos])

    return x


#determine which digit the given slice belongs to
def getDigit(digits: list[Digit], slice: Slice, tollarance: int) -> Digit:

    target = slice.getVerticies()
    
    for i in range(len(digits)):        
        digit = digits[i]

        #loops through all slices inside the digit
        for j in range(len(digit.slices)):
            testSlice = digit.slices[j]
            verts = testSlice.getVerticies()

            #loops through the two target verticies and compares them with the 2 test verticies
            for i in range(len(target)):
                vert = target[i]
                difX1 = np.abs([ vert[0] - verts[0][0]])
                difY1 = np.abs([ vert[1] - verts[0][1]])

                difX2 = np.abs([ vert[0] - verts[1][0]])
                difY2 = np.abs([ vert[1] - verts[1][1]])

                if difX1 < tollarance and difY1 < tollarance:
                    return digit
                if difX2 < tollarance and difY2 < tollarance:
                    return digit
                
    return None


#validate the digits sorted from left to right
#hTollarance is minimum distance required between digits
def validateDigits(digits: list[Digit], hTollarance) -> bool:

    valid = True
    count = len(digits)

    #4 digits includes values up to 999.9kg
    if count < 2 or count > 4: 
        return False 

    for i in range(count):
        digit = digits[i]
        sCount = len(digit.slices)
        verticals: list[Slice] = list(filter(lambda x: x.isVert == True, digit.slices))
        horizontals: list[Slice] = list(filter(lambda x: x.isVert == False, digit.slices))
        vCount = len(verticals)
        hCount = len(horizontals)

        #check that identified digits are not too close
        if i < count - 1:
            nextDigit = digits[i + 1]
            xRight = digit.getXmax()
            xLeft = nextDigit.getXmin()

            if np.abs(xRight - xLeft) < hTollarance:
                return False

        if sCount < 2 or sCount > 7: 
            return False
        
        if vCount < 2:
            return False  

        yMax = digit.getYmin()
        yMin = digit.getYmax()
        avgH = np.mean([ x.h for x in verticals ])
        digitHeight = np.abs(yMax - yMin)    

        #check that total height is equal to 2 stacked vertical slices
        if digitHeight < 1.75 * avgH:
            return False

        #validations for number 1, difficult to do elsewhere
        if sCount == 2 and vCount == 2:
            xMin = np.min([ x.xMin for x in verticals ])
            xMax = np.max([ x.xMax for x in verticals ])
            width = np.mean([ x.w for x in verticals ])

            #checks if the 2 verticals are in line with each other
            if xMax - xMin > 2 * width:
                valid = False

    return valid  



#estimates a suitable tollarance value based on dimensions of slices
def getTollarance(slices: list[Slice]) -> int:

    avg: list[float] = []

    for i in range(len(slices)):
        slice = slices[i]
        if slice.isVert:
            avg.append(slice.h)
    
    if len(avg) == 0:
        return 5
    
    avg = np.intp(np.mean(avg))
    return avg / 5



#contours is an array of slices defining different digits
def defineText(contours):

    slices: list[Slice] = []

    #each digit defines a number. Each number is composed of 2 to 7 slices
    #each contour defines a slice of 1 or more digits
    #to simplify comparisons, each slice is simplified / conseptulaised as a line
    #the analogue screen consists of two types of slices, vertical and horizontal

    #first we generate all slices
    for i in range(len(contours)):

        contour = contours[i]

        xVals = getVals(contour, 0)
        yVals = getVals(contour, 1)

        xMax = np.max(xVals)
        xMin = np.min(xVals)
        yMax = np.max(yVals)
        yMin = np.min(yVals)
        
        slice = Slice(contour, xMax, xMin, yMax, yMin)
        slices.append(slice)


    digits: list[Digit] = []
    tollarance = getTollarance(slices)

    #loop through slices, validate, and assign to corresponding digits
    for i in range(len(slices)):
        slice = slices[i]

         #first slice, create new digit
        if len(digits) == 0:
            digits.append(Digit(slice))  
        else:
            #determine which digit the slice belongs to
            digit = getDigit(digits, slice, tollarance)
            if digit == None:
                digits.append(Digit(slice))  
            else:
                digit.slices.append(slice)      
    

    #return the x value of the first verticie of the first slice
    def sortFunc(e: Digit):
        return e.getXmax()
    
    filtered = filter(lambda x: len(x.slices) > 0, digits)
    _sorted = sorted(filtered, reverse=False, key=sortFunc)

    if validateDigits(_sorted, tollarance / 2) == False:
        return None

    # for i in range(len(_sorted)):
    #     digit = _sorted[i]
    #     for slice in digit.slices:
    #         print('digit: ' + str(i) + ' slices:' + str(len(digit.slices)) + slice.toJSON() )

    finalValue: float = 0
    count = len(_sorted)
    power = count - 2
    sf = np.power(10, power, dtype=float)

    for i in range(count):
        digit = _sorted[i]
        value = digitToText(digit)

        if value == None:
            return None
        else:
            finalValue += value * sf
        
        sf = sf / 10

    #final bit of validation
    if finalValue > 300 or finalValue < 0:
        return None

    return finalValue
