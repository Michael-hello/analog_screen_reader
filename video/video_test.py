import numpy as np
import cv2
import pytesseract
from helpers import fileName

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

vidcap = cv2.VideoCapture('./data/test2.mp4');
success,frame = vidcap.read()
framenbr = 0

while success:
    success,frame = vidcap.read()
    framenbr = framenbr + 1
    if not success:
        break    

    if framenbr % 100 == 0:
        
        name = fileName(str(framenbr) + '_original')
        # cv2.imwrite(name, frame)

        
        name = fileName(str(framenbr))
        # cv2.imwrite(name, output)
    


# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
# data = pytesseract.image_to_string(gray, lang='eng', config='--psm 6')