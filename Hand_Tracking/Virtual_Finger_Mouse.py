import cv2
import numpy as np
import Hand_Tracking_Module as Htm
import time
from pyautogui import size, moveTo, click

########################################
wCam, hCam = 640, 480          # WebCam Resolution
wScr, hScr = size()            # Screen Resolution - pyautogui function
frameR = 100                   # Frame Reduction
smoothening = 5
########################################

pTime = 0
x3, y3 = 0, 0
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0
flag = True

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = Htm.HandDetector()

while True:
    success, img = cap.read()
    # Find Hand Landmarks
    img = detector.find_hands(img)
    lmList, bbox = detector.find_position(img)

    if len(lmList) != 0:
        # Get the tip of middle and index finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingers_up()

        # Region of Mouse movement
        top_left = (frameR, 0)
        bottom_right = (wCam, hCam-frameR-50)
        cv2.rectangle(img, top_left, bottom_right, (255, 0, 255), 3)

        # Only Index Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # Convert our Coordinates
            x3 = np.interp(x1, (top_left[0], bottom_right[0]), (0, wScr))
            y3 = np.interp(y1-5, (top_left[1], bottom_right[1]), (0, hScr))

            # Smoothen values
            cLocX = pLocX + (x3-pLocX)//smoothening
            cLocY = pLocY + (y3-pLocY)//smoothening
            pLocX, pLocY = cLocX, cLocY

            # Move Mouse - pyautogui function
            moveTo(wScr-cLocX, cLocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

        # Both Index and Middle Fingers: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # Find distance b/w the fingers
            img, length, line_info = detector.find_distance(img, 8, 12)

            # Click Mouse if distance short
            if length < 40:
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                # flag is used so that it clicks only once
                if flag:
                    flag = False
                    click()  # pyautogui function
            elif length >= 40:
                flag = True

    # Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime+0.001)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
