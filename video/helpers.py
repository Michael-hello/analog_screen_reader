import numpy as np
import cv2
import os, shutil


def fileName(label: str) -> str:
    location = "./results/"
    return location + label + ".png"


def showInWindow(winname, img, x, y, text = None):
    image = cv2.resize(img.copy(), (0,0), fx=0.5, fy=0.5)
    cv2.namedWindow(winname)      
    cv2.moveWindow(winname, x, y) 

    if text != None:
        image = cv2.putText(image, text, (00, 185) , cv2.FONT_HERSHEY_SIMPLEX , 1, 
                  (0, 0, 255), 2, cv2.LINE_AA, True) 
        
    cv2.imshow(winname,image)


#converts float to an integer >= to 0
def makeSafe(x: float) -> int:
    int = np.intp(x)
    return np.max([ 0, int ])


#save image to results folder
def saveImage(image, label):
    _fileName = fileName(label)
    cv2.imwrite(_fileName, image)


#delete all files in a directory
def deleteAllFiles(folder):
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

#rounds a float to 1 DP
def formatValue(x: float) -> str:
    if x == None:
        return ''
    rounded = np.round([ x * 10])
    return str(rounded[0] / 10)


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