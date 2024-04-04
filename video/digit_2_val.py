import numpy as np
from digits import Digit, Slice


def digitParams(digit: Digit) -> dict:

    #need to determine if the vertical slices are on the left or the right of the digit
    verticals: list[Slice] = list(filter(lambda x: x.isVert == True, digit.slices))
    horizontals: list[Slice] = list(filter(lambda x: x.isVert == False, digit.slices))

    slices = digit.slices
    count = len(slices)
    vCount = len(verticals)
    hCount = len(horizontals)

    #position of horizontal slice. h1 = top. h2 = mid. h3 = bot
    h1 = False
    h2 = False
    h3 = False

    #position of vertical slices. v1 = top left. v2 = top right. v3 = bottom left. v4 = bottom right
    v1 = False
    v2 = False
    v3 = False
    v4 = False

    # if hCount >= 1 and hCount <= 3 and vCount >= 2 and vCount <= 4:
    
    #     avgLeftX = 0
    #     avgRightX = 0
    #     top = horizontals[0].yMin
    #     bot = horizontals[0].yMax

    #     # loop through h slices to determine diemsnions of the digit
    #     for slice in horizontals:
    #         avgLeftX += slice.xMin
    #         avgRightX += slice.xMax
    #         if slice.yMin < top:
    #             top = slice.yMin
    #         if slice.yMax > bot:
    #             bot = slice.yMax

    #     leftX = avgLeftX / len(horizontals)
    #     rightX = avgRightX / len(horizontals)

    #     leftVert: list[Slice] = []
    #     rightVert: list[Slice] = []

    #     #decide if vertical slices are on the left or right of the digit
    #     for vert in verticals:
    #         avgX = (vert.xMax + vert.xMin) / 2
    #         diffLeft = np.abs(leftX - avgX)
    #         diffRight = np.abs(rightX - avgX)
    #         if diffLeft < diffRight:
    #             leftVert.append(vert)
    #         else:
    #             rightVert.append(vert)

    #     #2 right slices therefore is 3
    #     if len(rightVert) == 2:
    #         return 3
        
    #     #if left vertical is top then is 5, otherwise is 2
    #     if (len(leftVert)) == 1:
    #         left: Slice = leftVert[0]
    #         avgY = (left.yMax + left.yMin) / 2
    #         diffTop = np.abs(top - avgY)
    #         diffBot = np.abs(bot - avgY)
    #         if diffTop < diffBot:
    #             return 5
    #         else:
    #             return 2

    params =  {
        'count': count,
        'vCount': vCount,
        'hCount': hCount,
        'h1' : h1,
        'h2' : h2,
        'h3' : h3,
        'v1' : v1,
        'v2' : v2,
        'v3' : v3,
        'v4' : v4
    }

    return params, count, hCount, vCount

#checks if a given digit passes the below validations
def isValid(params: dict, count: int, vCount: int, hCount: int):

    valid = True

    if hCount + vCount != count:
        ValueError('Invalid count params')

    if count != params['count']: valid = False
    if hCount != params['hCount']: valid = False
    if vCount != params['vCount']: valid = False

    return valid



def digitToText(digit: Digit) -> int:

    params, count, hCount, vCount = digitParams(digit)

    if count < 2 or count > 7:
        return None

    if isValid(params, count= 2, vCount= 2, hCount= 0):
        return 1   
    
    if isValid(params, count= 7, vCount= 4, hCount= 3):
        return 8 
 
    if isValid(params, count= 4, vCount= 3, hCount= 1):     
        return 4

    if isValid(params, count= 3, vCount= 2, hCount= 1):
        return 7

    if isValid(params, count= 6, vCount= 3, hCount= 3):
        return 6

    if isValid(params, count= 6, vCount= 4, hCount= 2):
        return 0
    
    if isValid(params, count= 5, vCount= 3, hCount= 2):  
        return 9

    if isValid(params, count= 5, vCount= 2, hCount= 3):
        
        #TO DO: remove this and finish digitParams
        verticals: list[Slice] = list(filter(lambda x: x.isVert == True, digit.slices))
        horizontals: list[Slice] = list(filter(lambda x: x.isVert == False, digit.slices))

        avgLeftX = 0
        avgRightX = 0
        top = horizontals[0].yMin
        bot = horizontals[0].yMax

        # loop through h slices to determine diemsnions of the digit
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

