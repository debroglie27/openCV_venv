import cv2
import numpy as np

img = cv2.imread("../Photos/lena.png")
kernel = np.ones((5, 5), np.uint8)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)
imgCanny = cv2.Canny(img, 100, 100)
# Kernel can be of all ones like the 5th line
imgDilate = cv2.dilate(imgCanny, (5, 5), iterations=3)
imgErode = cv2.erode(imgDilate, (5, 5), iterations=3)

cv2.imshow("Gray Image", imgGray)
cv2.imshow("Blur Image", imgBlur)
cv2.imshow("Canny Image", imgCanny)
cv2.imshow("Dilated Image", imgDilate)
cv2.imshow("Eroded Image", imgErode)

cv2.waitKey(0)
