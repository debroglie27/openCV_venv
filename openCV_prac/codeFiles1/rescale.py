import cv2 as cv


def rescale_frame(f, scale=0.75):
    width = int(f.shape[1] * scale)
    height = int(f.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(f, dimensions, interpolation=cv.INTER_AREA)


# img = cv.imread('./Photos/cat.jpg')
# # cv.imshow('Cat', img)
# resized_img = rescale_frame(img)
# cv.imshow('Cat', resized_img)
# cv.waitKey(0)


# Resolution will only change for LIVE Videos
def change_res(width, height):
    capture.set(3, width)
    capture.set(4, height)


capture = cv.VideoCapture('../Videos/dog.mp4')

while True:
    isTrue, frame = capture.read()

    frame_resized = rescale_frame(frame)

    # cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()
