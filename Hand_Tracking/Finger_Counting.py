import cv2
import time
import os
import Hand_Tracking_Module as Htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# Making a list of the name of the Finger Images
folder_path = "Finger_Images"
myList = os.listdir(folder_path)

# Reading the Images and storing in the Overlay list
overlay_list = []
for imPath in myList:
    image = cv2.imread(f'{folder_path}/{imPath}')
    overlay_list.append(image)

# Initialising our Hand Detector Object
detector = Htm.HandDetector(detection_conf=0.75)

# These Ids correspond to the Tips of the 5 fingers
tip_ids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)

    if len(lm_list) != 0:
        # List of fingers which are up
        fingers = detector.fingers_up()

        # Counting Total Fingers from the fingers list
        total_fingers = fingers.count(1)

        # Image of Hand corresponding to the number value
        h, w, c = overlay_list[total_fingers-1].shape
        img[0:h, 0:w] = overlay_list[total_fingers-1]

        # Number Value Displayed
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(total_fingers), (45, 395), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 20)

    # For the FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime + 0.001)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (480, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)
