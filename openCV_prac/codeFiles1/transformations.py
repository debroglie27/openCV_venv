import cv2 as cv
import numpy as np

img = cv.imread('../Photos/park.jpg')

cv.imshow('Boston', img)


# Translations (shifting along x and y axis)
def translate(image, x, y):
    trans_mat = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (image.shape[1], image.shape[0])
    return cv.warpAffine(image, trans_mat, dimensions)


# -x --> LEFT
# -y --> UP
# +x --> RIGHT
# +y --> DOWN

translated = translate(img, 100, 100)
cv.imshow('Translated', translated)


# Rotations
def rotate(image, angle, rot_point=None):
    (height, width) = image.shape[:2]

    if rot_point is None:
        rot_point = (width//2, height//2)

    rot_mat = cv.getRotationMatrix2D(rot_point, angle, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(image, rot_mat, dimensions)


rotated = rotate(img, 45)
cv.imshow('Rotated', rotated)


# Resizing
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resized)


# Flipping
# 0 --> Vertically
# 1 --> Horizontally
# -1 --> Both
flip = cv.flip(img, -1)
cv.imshow("Flipped", flip)


# Cropping
cropped = img[200:400, 300:500]
cv.imshow('Cropped', cropped)

cv.waitKey(0)
