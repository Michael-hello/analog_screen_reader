import numpy as np
import cv2


def fileName(label: str) -> str:
    location = "./results/"
    return location + label + ".png"


def showInWindow(winname, img, x, y):
    image = cv2.resize(img, (0,0), fx=0.25, fy=0.25)
    cv2.namedWindow(winname)      
    cv2.moveWindow(winname, x, y) 
    cv2.imshow(winname,image)

