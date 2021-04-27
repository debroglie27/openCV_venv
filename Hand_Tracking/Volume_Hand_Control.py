import cv2
import time
import numpy as np
import Hand_Tracking_Module as Htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Used For Volume Change
###############################################################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
###############################################################

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = Htm.HandDetector(detection_conf=0.7)
pTime = 0
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)

    # If the lm_list is not empty
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])

        # Coordinates for Tip of Index and Thumb
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        # Coordinate of midpoint between those 2 points above
        cx, cy = (x1+x2)//2, (y1+y2)//2

        # Circles for Tip of Index and Thumb
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # Circle between Index Tip and Thumb Tip
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        # Line between Index Tip and Thumb Tip
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Length of the Line
        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand Range: 30 - 300
        # Volume Range: -65 - 0
        # interp function used to convert a value in a particular range to a different range
        vol = np.interp(length, [30, 240], [minVol, maxVol])
        volBar = np.interp(length, [30, 240], [400, 150])
        volPer = np.interp(length, [30, 240], [0, 100])
        # For Setting the Volume
        volume.SetMasterVolumeLevel(vol, None)

        # When the length goes below 30 the midpoint circle becomes Green
        if length < 30:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Volume Box shown in the Webcam
    cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 1)
    cv2.rectangle(img, (51, int(volBar)), (84, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}', (48, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # For the FPS
    cTime = time.time()
    fps = 1/(cTime-pTime+0.001)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 45), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
