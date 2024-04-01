import cv2 
import numpy as np
import json
import uuid

class Slice:
                                
    def __init__(self, contour, xMax, xMin, yMax, yMin):
        self.contour = contour
        self.xMax = xMax
        self.xMin = xMin
        self.yMax = yMax
        self.yMin = yMin
        self.h = yMax - yMin
        self.w = xMax - xMin
        #if a slice is a vertical or horizotnal orientation
        self.isVert = self.h > 1.5 * self.w

    #to simplify comparisons, a slice is treated as a line with 2 end points
    def getVerticies(self):

        if self.isVert:
            xAvg = (self.xMax + self.xMin) / 2
            return [ [ xAvg, self.yMin ], [ xAvg, self.yMax ] ]
        else:
            yAvg = (self.yMax + self.yMin) / 2
            return [ [ self.xMin, yAvg ], [ self.xMax, yAvg ] ]
        
    def toJSON(self):
        dict = {
            'xMax' :   float(self.xMax),
            'xMin' :   float(self.xMin),
            'yMax' :   float(self.yMax),
            'yMin' :   float(self.yMin),
            'h' :      float(self.h),
            'w' :      float(self.w),
            'type' : 'vertical' if self.isVert else 'horizontal'
        }
        return json.dumps(dict)


#digit currently is just a collection of slices
class Digit:

    def __init__(self, slice: Slice):
        self.slices = [ slice ]
        self.id = uuid.uuid4()

    def toJSON(self):
        list = []
        for slice in self.slices:
            list.append(slice.toJSON())
        return list



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
    vCount = len(list(filter(lambda x: x.isVert == True, slices)))
    hCount = len(list(filter(lambda x: x.isVert == False, slices)))

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
    
    if count == 5 and vCount == 2 and hCount == 3:
        #need to determine if the vertical slices are on teh left or the right of the digit
        verticals: list[Slice] = list(filter(lambda x: x.isVert == True, slices))
        horizontals: list[Slice] = list(filter(lambda x: x.isVert == False, slices))
        
        avgLeftX = 0
        avgRightX = 0
        top = horizontals[0].yMin
        bot = horizontals[0].yMax

        # loop through 3 h slices to determine diemsnions of the digit
        for slice in horizontals:
            avgLeftX += slice.xMin
            avgRightX += slice.xMax
            if slice.yMin < top:
                top = slice.yMin
            if slice.yMax > bot:
                bot = slice.yMax

        leftX = avgLeftX / len(horizontals)
        rightX = avgRightX / len(horizontals)

        leftVert: list[Slice] = []
        rightVert: list[Slice] = []

        #decide if vertical slices are on the left or right of the digit
        for vert in verticals:
            avgX = (vert.xMax + vert.xMin) / 2
            diffLeft = np.abs(leftX - avgX)
            diffRight = np.abs(rightX - avgX)
            if diffLeft < diffRight:
                leftVert.append(vert)
            else:
                rightVert.append(vert)

        #2 right slices therefore is 3
        if len(rightVert) == 2:
            return 3
        
        #if left vertical is top then is 5, otherwise is 2
        if (len(leftVert)) == 1:
            left: Slice = leftVert[0]
            avgY = (left.yMax + left.yMin) / 2
            diffTop = np.abs(top - avgY)
            diffBot = np.abs(bot - avgY)
            if diffTop < diffBot:
                return 5
            else:
                return 2
        
    return None


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

        #epsilon of 50 used, this is the max number of verticies
        contour2 = cv2.approxPolyDP(contours[i], 50, True)

        xVals = getVals(contour2, 0)
        yVals = getVals(contour2, 1)

        xMax = np.max(xVals)
        xMin = np.min(xVals)
        yMax = np.max(yVals)
        yMin = np.min(yVals)
        
        slice = Slice(contour2, xMax, xMin, yMax, yMin)
        slices.append(slice)


    digits: list[Digit] = []
    tollarance = getTollarance(slices)

    #loop through slices and assign to corresponding digits
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
        verts = e.slices[0].getVerticies()
        return verts[0][0]
    
    filtered = filter(lambda x: len(x.slices) > 0, digits)
    _sorted = sorted(filtered, reverse=False, key=sortFunc)

    for i in range(len(_sorted)):
        digit = _sorted[i]
        for slice in digit.slices:
            print('digit: ' + str(i) + ' slices:' + str(len(digit.slices)) + slice.toJSON() )

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
