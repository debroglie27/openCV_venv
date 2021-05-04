import cv2
import mediapipe as mp
import time
import numpy as np
import math


class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.detectionConf = detection_conf
        self.trackConf = track_conf

        # Required for initialisation
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

        # These Ids correspond to the Tips of the 5 fingers
        self.tip_ids = [4, 8, 12, 16, 20]

        blank = np.zeros((640, 480, 3), dtype="uint8")
        self.results = self.hands.process(blank)
        self.lm_list = []

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_num=0, points_draw=False, bbox_draw=True):
        xList = []
        yList = []
        self.lm_list = []
        bbox = ()

        if self.results.multi_hand_landmarks:
            # Finding Position of given Hand
            my_hand = self.results.multi_hand_landmarks[hand_num]

            for _id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                # Pixel Position for corresponding landmark
                cx, cy = int(lm.x * w), int(lm.y * h)

                xList.append(cx)
                yList.append(cy)
                self.lm_list.append([_id, cx, cy])

                if points_draw:
                    cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)

            xMin, xMax = min(xList), max(xList)
            yMin, yMax = min(yList), max(yList)
            bbox = xMin, yMin, xMax, yMax

            if bbox_draw:
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)

        return self.lm_list, bbox

    def fingers_up(self):
        ##############
        # Assuming No Horizontal Flip
        ##############
        if len(self.lm_list) == 0:
            return

        # This List will have 5 values corresponding to each of the 5 fingers
        # When a particular finger is open its value in the fingers list is 1,
        # Otherwise 0
        fingers = []

        # Thumb
        # Below Logic is to find whether the Hand is Left or Right
        if self.lm_list[4][1] > self.lm_list[17][1]:
            # Right Hand Thumb
            if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Left Hand Thumb
            if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers
        for _id in range(1, 5):
            if self.lm_list[self.tip_ids[_id]][2] < self.lm_list[self.tip_ids[_id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def find_distance(self, img, p1, p2, draw=True):
        # Coordinates for ids p1 and p2
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        # Coordinate of midpoint between those 2 points above
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            # Circles for ids p1 and p2
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            # Circle between ids p1 and p2
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
            # Line between ids p1 and p2
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        # Length of the Line
        length = math.hypot(x2 - x1, y2 - y1)

        return img, length, [x1, y1, x2, y2, cx, cy]

    def detect_hand_type(self, flip=False):
        if self.lm_list[4][1] > self.lm_list[17][1]:
            # Right Hand if flip -> False
            # Left  Hand if flip -> True
            return "Left" if flip else "Right"
        else:
            # Left  Hand if flip -> False
            # Right Hand if flip -> True
            return "Right" if flip else "Left"


def main():
    cap = cv2.VideoCapture(0)
    # Prev Time used in display FPS
    pTime = 0
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)

        # list of all the hand landmarks along with position
        lm_list, bbox = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[4])

        # Here Calculation of FPS done
        cTime = time.time()
        fps = 1 / (cTime - pTime + 0.003)
        pTime = cTime

        # Displaying of Calculated FPS
        # (Image, string to put, position, font, scale, color, thickness)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
