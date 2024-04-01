import cv2 
import numpy as np

class Slice:
                                
    def __init__(self, isVert, contour, xMax, xMin, yMax, yMin):
        self.isVert = isVert
        self.contour = contour
        self.xMax = xMax
        self.xMin = xMin
        self.yMax = yMax
        self.yMin = yMin
    
    #to simplify comparisons, a slice is treated as a line with 2 end points
    def getVerticies(self):

        if self.isVert:
            xAvg = (self.xMax + self.xMin) / 2
            return [ [ xAvg, self.yMin ], [ xAvg, self.yMax ] ]
        else:
            yAvg = (self.yMax + self.yMin) / 2
            return [ [ self.xMin, yAvg ], [ self.xMax, yAvg ] ]


#digit currently is just a collection of slices
class Digit:

    def __init__(self, slice: Slice):
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

    if count < 2 or count > 7:
        return None

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


#estimates a suitable tollarance value based on dimensions of slices
def getTollarance(contours) -> int:

    avg: list[float] = []
    i = 0

    while len(avg) < 5 and i < len(contours) - 1:
        #to do make this more efficient?
        i += 1
        contour2 = cv2.approxPolyDP(contours[i], 10, True)
        x, y, w, h = cv2.boundingRect(contour2)
        isVert = h > 1.5 * w
        # print(isVert, x, y , w ,h)
        if isVert:
            avg.append(h)
    
    if len(avg) == 0:
        return 5
    
    avg = np.intp(np.mean(avg))
    return avg / 5



#contours is an array of slices defining different digits
def defineText(contours):

    digits: list[Digit] = []
    tollarance = getTollarance(contours)

    #each digit defines a number. Each number is composed of 2 to 7 slices
    #each contour defines a slice of 1 or more digits
    #to simplify comparisons, each slice is simplified / conseptulaised as a line
    #the analogue screen consists of two types of slices, vertical and horizontal

    for i in range(len(contours)):

        #epsilon of 10 used, this is the max number of verticies
        contour2 = cv2.approxPolyDP(contours[i], 10, True)
        x, y, w, h = cv2.boundingRect(contour2)

        xVals = getVals(contour2, 0)
        yVals = getVals(contour2, 1)

        xMax = np.max(xVals)
        xMin = np.min(xVals)
        yMax = np.max(yVals)
        yMin = np.min(yVals)

        isVert = h > 1.5 * w
        slice = Slice(isVert, contour2, xMax, xMin, yMax, yMin)

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
        verts = e.slices[0].getVerticies()
        return verts[0][0]
    
    filtered = filter(lambda x: len(x.slices) > 0, digits)
    _sorted = sorted(filtered, reverse=False, key=sortFunc)

    finalValue = 0
    count = len(_sorted)
    power = count - 2
    sf = np.power(10, power, dtype=float)

    for i in range(count):
        digit = _sorted[i]
        value = digitToText(digit)

        if value != None:
            finalValue += value * sf
        
        sf = sf / 10

    print(finalValue)
    return finalValue
