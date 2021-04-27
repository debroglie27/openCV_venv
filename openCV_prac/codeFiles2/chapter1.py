import cv2

# # Reading Images
# img = cv2.imread("../Photos/lena.png")
# cv2.imshow('Image of Lena', img)
#
# cv2.waitKey(0)

# # Reading Video Files
# cap = cv2.VideoCapture("../Videos/dog.mp4")
#
# while True:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break

# Webcam
cap = cv2.VideoCapture(0)
# Width
cap.set(3, 640)
# Height
cap.set(4, 480)
# Brightness
cap.set(10, 50)

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
