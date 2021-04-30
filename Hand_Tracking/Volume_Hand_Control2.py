import cv2
import time
import numpy as np
import Hand_Tracking_Module as Htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Used For Volume Change
###############################################################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# noinspection PyTypeChecker
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
###############################################################

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = Htm.HandDetector(detection_conf=0.7)
pTime = 0
vol = 0
volBar = 399
volPer = 0
volColor = (255, 0, 0)

while True:
    success, img = cap.read()

    # Find Hand
    img = detector.find_hands(img)
    lm_list, bbox = detector.find_position(img)

    # If list is empty
    if len(lm_list) == 0:
        volColor = (255, 0, 0)
    # If the lm_list is not empty
    else:
        # Filter based on size
        area = ((bbox[2]-bbox[0]) * (bbox[3]-bbox[1])) // 100

        if 250 < area < 1100:
            # Find distance between Index and Thumb
            img, length, line_info = detector.find_distance(img, 4, 8)

            # Convert Volume
            # Hand Range: 30 - 300
            # Volume Range: -65 - 0
            # interp function used to convert a value in a particular range to a different range
            volBar = np.interp(length, [30, 200], [400, 150])
            volPer = np.interp(length, [30, 200], [0, 100])

            # Reduce Resolution to make it smother
            smoothness = 5
            volPer = smoothness * (volPer//smoothness)

            # Check fingers up
            fingers = detector.fingers_up()

            # If pinky finger down then set volume
            if not fingers[4]:
                # For Setting the Volume
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                # Indication that Volume is Set, by drawing green circle at midpoint circle
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                volColor = (0, 255, 0)
            else:
                volColor = (255, 0, 0)

    # Volume Box shown in the Webcam
    cv2.rectangle(img, (50, 149), (85, 400), (0, 0, 255), 1)
    cv2.rectangle(img, (51, int(volBar)), (84, 399), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}', (48, 440), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # Our System Volume Shown
    current_volume = round(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Vol Set: {current_volume}', (400, 45), cv2.FONT_HERSHEY_COMPLEX, 1, volColor, 2)

    # For the FPS
    cTime = time.time()
    fps = 1/(cTime-pTime+0.001)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 45), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
