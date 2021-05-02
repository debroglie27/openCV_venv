import cv2
import mediapipe as mp
import time
import numpy as np


class FaceMeshDetector:
    def __init__(self, static_mode=False, max_faces=2, min_detection_conf=0.5, min_track_conf=0.5):
        self.static_mode = static_mode
        self.max_faces = max_faces
        self.min_detection_conf = min_detection_conf
        self.min_track_conf = min_track_conf

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.static_mode, self.max_faces,
                                                 self.min_detection_conf, self.min_track_conf)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

        # Default blank image
        blank = np.zeros((640, 480, 3), dtype="uint8")
        self.results = self.faceMesh.process(blank)

    def find_face_mesh(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        faces = []

        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACE_CONNECTIONS, self.drawSpec, self.drawSpec)

                face = []
                for _id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    face.append([x, y])

                faces.append(face)

        return img, faces


def main():
    cap = cv2.VideoCapture("./Videos/6.mp4")
    pTime = 0

    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img, faces = detector.find_face_mesh(img)

        if len(faces) != 0:
            print(len(faces))

        cTime = time.time()
        fps = 1 / (cTime - pTime + 0.001)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
