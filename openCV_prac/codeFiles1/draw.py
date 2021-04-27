import cv2 as cv
import numpy as np

# uint8 is the datatype for image
blank = np.zeros((500, 500, 3), dtype="uint8")
# cv.imshow('Blank', blank)

# 1. Painting the image a certain color
# blank[100:200, 200:400] = 0, 0, 255      # BGR
# cv.imshow('Certain Color', blank)

# 2. Draw a Rectangle
# cv.rectangle(blank, (0, 0), (250, 250), (0, 255, 0), thickness=2)
# cv.rectangle(blank, (0, 0), (250, 250), (0, 255, 0), thickness=cv.FILLED)
cv.rectangle(blank, (0, 0), (blank.shape[1]//2, blank.shape[0]//2), (0, 255, 0), thickness=cv.FILLED)
# cv.imshow('Rectangle', blank)

# 3. Draw a Circle
cv.circle(blank, center=(250, 250), radius=40, color=(0, 0, 255), thickness=cv.FILLED)
cv.imshow('Circle', blank)

# 4. Draw a Line
cv.line(blank, (0, 0), (250, 250), (255, 255, 255), thickness=3)
cv.imshow('Line', blank)

# 5. Write Text in image
cv.putText(blank, "Hello", (210, 320), cv.FONT_HERSHEY_TRIPLEX, 1.0, (255, 0, 0), thickness=2)
cv.imshow('Text', blank)

cv.waitKey(0)
