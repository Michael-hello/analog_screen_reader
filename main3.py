import numpy as np
import cv2

print('running..')

inputImage = cv2.imread("OPTV_39.9_70.0.png")

# Convert to graycsale
img_gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (7,7), 0) 

# Blur the image for better edge detection

# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200, apertureSize=3, L2gradient=True)

minLineLength = 10
maxLineGap = 10

lines = cv2.HoughLinesP(edges,cv2.HOUGH_PROBABILISTIC, np.pi/180, 30, minLineLength,maxLineGap)

for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        #cv2.line(inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
        pts = np.array([[x1, y1 ], [x2 , y2]], np.int32)
        cv2.polylines(inputImage, [pts], True, (0,255,0))


# cv2.imshow("Trolley_Problem_Result", inputImage)
# cv2.imshow('edge', edges)

cv2.imwrite("./out_canny3.png", inputImage)


# cv2.imshow('Canny Edge Detection', canny)
# cv2.imwrite("./out_canny2.png", edges)
# cv2.waitKey(0)

print('finished..')