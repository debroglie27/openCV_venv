import cv2
import numpy as np
import os
import Hand_Tracking_Module as Htm

folder_path = "Header_Images"
myList = os.listdir(folder_path)

overlay_list = []
for imPath in myList:
    image = cv2.imread(f'{folder_path}/{imPath}')
    overlay_list.append(image)

########################################
header = overlay_list[0]
# Default Red
draw_color = (0, 0, 255)
# Default 15
brush_thickness = 15
# Default 50
eraser_thickness = 50
########################################

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = Htm.HandDetector(detection_conf=0.8)
img_canvas = np.zeros((480, 640, 3), np.uint8)
xp, yp = 0, 0

while True:
    # Import Image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    cv2.line(img, (120, 0), (120, 96), (255, 0, 0), 3)
    cv2.line(img, (240, 0), (240, 96), (255, 0, 0), 3)
    cv2.line(img, (360, 0), (360, 96), (255, 0, 0), 3)
    cv2.line(img, (480, 0), (480, 96), (255, 0, 0), 3)

    if len(lmList) != 0:
        # Tip of Index and Middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are Up
        fingers = detector.fingers_up()

        # Selection Mode: Index and Middle fingers up
        if fingers[1] and fingers[2]:
            # Resetting x_prev and y_prev
            xp, yp = 0, 0

            # Checking for Click
            if y1 < 96:
                if x1 <= 120:
                    # Red Color
                    header = overlay_list[0]
                    draw_color = (0, 0, 255)
                elif 240 >= x1 > 120:
                    # Green Color
                    header = overlay_list[1]
                    draw_color = (0, 255, 0)
                elif 360 >= x1 > 240:
                    # Blue Color
                    header = overlay_list[2]
                    draw_color = (255, 0, 0)
                elif 480 >= x1 > 360:
                    # Yellow Color
                    header = overlay_list[3]
                    draw_color = (0, 255, 255)
                else:
                    # Eraser
                    header = overlay_list[4]
                    draw_color = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)

        # Drawing Mode: Index finger up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # For Eraser different thickness
            if draw_color == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), draw_color, eraser_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, eraser_thickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), draw_color, brush_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)

            xp, yp = x1, y1

    # Below Code used for combining out Canvas and Webcam Image
    imgGray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, img_canvas)

    # Setting the Header Image
    img[0:96, 0:640] = header

    cv2.imshow('Virtual Finger Painter', img)
    cv2.waitKey(1)
