import cv2 
import numpy as np
import time

def findText(cropped, lower, upper):
    
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    _, th2 = cv2.threshold(gray, lower, upper, 0)
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        cropped = cv2.drawContours(cropped, contours, i, (50, 250, 50), 2)

    return cropped