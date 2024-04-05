import numpy as np
import json
import uuid


#a slice is one of 7 possible horizontal or vertical segments that define an analogue digit
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




class Digit:

    def __init__(self, slice: Slice):
        self.slices = [ slice ]
        self.id = uuid.uuid4()

    def toJSON(self):
        list = []
        for slice in self.slices:
            list.append(slice.toJSON())
        return list
    
    #returns maximum x val of all slices
    def getXmax(self):
        return np.max([ x.xMax for x in self.slices ])

    #returns min x val of all slices
    def getXmin(self):
        return np.min([ x.xMin for x in self.slices ])
    
    #returns maximum y val of all slices
    def getYmax(self):
        return np.max([ x.yMax for x in self.slices ])

    #returns min y val of all slices
    def getYmin(self):
        return np.min([ x.yMin for x in self.slices ])

