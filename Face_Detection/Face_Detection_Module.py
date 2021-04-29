import cv2
import mediapipe as mp
import time
import numpy as np


class FaceDetector:
    def __init__(self, min_detection_conf=0.5):
        self.min_detection_conf = min_detection_conf

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.min_detection_conf)

        # Default blank image
        blank = np.zeros((640, 480, 3), dtype="uint8")
        self.results = self.faceDetection.process(blank)

    def find_faces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results)

        bounding_boxes = []
        if self.results.detections:
            for _id, detection in enumerate(self.results.detections):

                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)

                bounding_boxes.append([_id, bbox, detection.score[0]])

                if draw:
                    # Fancy Bounding Box and Score Value
                    self.fancy_draw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        return img, bounding_boxes

    @staticmethod
    def fancy_draw(img, bbox, length=30, t=5, rt=1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        # Bounding Box
        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left  x,y
        cv2.line(img, (x, y), (x + length, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y + length), (255, 0, 255), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - length, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + length), (255, 0, 255), t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + length, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - length), (255, 0, 255), t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - length, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - length), (255, 0, 255), t)

        return img


def main():
    cap = cv2.VideoCapture("./Videos/1.mp4")
    pTime = time.time()

    detector = FaceDetector()

    while True:
        success, img = cap.read()
        img, bounding_boxes = detector.find_faces(img)

        if len(bounding_boxes) != 0:
            print(bounding_boxes)

        cTime = time.time()
        fps = 1 / (cTime - pTime + 0.0001)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
