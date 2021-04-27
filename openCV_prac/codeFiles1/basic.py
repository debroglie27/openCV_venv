import cv2 as cv

img = cv.imread('../Photos/park.jpg')
cv.imshow('Park', img)

# Converting to GrayScale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('Gray', gray)

# Blurring the image
blur = cv.GaussianBlur(img, ksize=(7, 7), sigmaX=cv.BORDER_DEFAULT)
# cv.imshow('Blur', blur)

# Edge Cascade
# canny = cv.Canny(img, 125, 175)
canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edges', canny)

# Dilating the image
dilated = cv.dilate(canny, (7, 7), iterations=3)
cv.imshow('Dilated', dilated)

# Eroding (opposite of dilating)
eroded = cv.erode(dilated, (7, 7), iterations=3)
cv.imshow('Eroded', eroded)

# Resize Images
# INTER_AREA -> when making the image small
# INTER_LINEAR -> when making image big
# INTER_CUBIC -> when making image big (slower but more effective)
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)
cv.imshow('Resized', resized)

# Cropping Images
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)

cv.waitKey(0)
