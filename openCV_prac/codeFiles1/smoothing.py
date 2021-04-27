import cv2 as cv

img = cv.imread('../Photos/cats.jpg')
cv.imshow('Cats', img)

# Averaging
average = cv.blur(img, (3, 3))
cv.imshow('Average Blur', average)

# Gaussian blur
gauss = cv.GaussianBlur(img, (3, 3), 0)
cv.imshow("Gaussian Blur", gauss)

# Median Blur
median = cv.medianBlur(img, 3)
cv.imshow("Median Blur", median)

# Bilateral Blur
bilateral = cv.bilateralFilter(img, 5, 15, 15)
cv.imshow("Bilateral Blur", bilateral)

cv.waitKey(0)
