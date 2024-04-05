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

    #this includes all valid digits other than 1
    #populate the above values
    if hCount >= 1 and hCount <= 3 and vCount >= 2 and vCount <= 4:

        xMax = digit.getXmax()
        xMin = digit.getXmin()
        yMax = digit.getYmax()
        yMin = digit.getYmin()

        for vert in verticals:
            avgX = (vert.xMax + vert.xMin) / 2
            avgY = (vert.yMax + vert.yMin) / 2

            diffLeft = np.abs(xMin - avgX)
            diffRight  = np.abs(xMax - avgX)
            diffTop = np.abs(yMin - avgY)
            diffBot = np.abs(yMax - avgY)

            isLeft = diffLeft < diffRight
            isTop = diffTop < diffBot

            if isLeft and isTop: v1 = True
            if isLeft == False and isTop: v2 = True
            if isLeft and isTop == False: v3 = True
            if isLeft == False and isTop == False: v4 = True

       
        for hori in horizontals:
            mid = np.mean([ yMax , yMin ])
            avgY = (hori.yMax + hori.yMin) / 2

            diffTop = np.abs(avgY - yMin)
            diffMid = np.abs(avgY - mid)
            diffBot = np.abs(avgY - yMax)
            all = [ diffTop, diffMid, diffBot ]

            if np.min(all) == diffTop: h1 = True
            if np.min(all) == diffMid: h2 = True
            if np.min(all) == diffBot: h3 = True
            

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
def isValid(
        params: dict, 
        count: int, 
        vCount: int = None, 
        hCount: int = None, 
        h1 = False,
        h2 = False,
        h3 = False,
        v1 = False,
        v2 = False,
        v3 = False,
        v4 = False ):

    valid = True

    if count != params['count']: valid = False

    if hCount != None and hCount != params['hCount']: valid = False
    if vCount != None and vCount != params['vCount']: valid = False

    if h1 and params['h1'] == False: valid = False 
    if h2 and params['h2'] == False: valid = False 
    if h3 and params['h3'] == False: valid = False 
    if v1 and params['v1'] == False: valid = False 
    if v2 and params['v2'] == False: valid = False 
    if v3 and params['v3'] == False: valid = False 
    if v4 and params['v4'] == False: valid = False 

    return valid



def digitToText(digit: Digit) -> int:

    params, count, vCount, hCount = digitParams(digit)

    if count < 2 or count > 7:
        return None

    if isValid(params, count= 2, vCount= 2, hCount= 0):
        return 1   
    
    if isValid(params, count= 7, vCount= 4, hCount= 3):
        return 8 
 
    if isValid(params, count= 4, h2=True, v1=True, v2=True, v4=True):     
        return 4

    if isValid(params, count= 3, h1=True, v2=True, v4=True):
        return 7

    if isValid(params, count= 6, h1=True, h3=True, v1=True, v2=True, v3=True, v4=True):
        return 0
    
    if isValid(params, count= 6, h1=True, h2=True, h3=True, v1=True, v3=True, v4=True):
        return 6
    
    if isValid(params, count= 6, h1=True, h2=True, h3=True, v1=True, v2=True, v4=True):  
        return 9

    if isValid(params, count= 5, h1=True, h2=True, h3=True, v2=True, v3=True):
        return 2
    
    if isValid(params, count= 5, h1=True, h2=True, h3=True, v2=True, v4=True):
        return 3

    if isValid(params, count= 5, h1=True, h2=True, h3=True, v1=True, v4=True):
        return 5   
     
    return None

