import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('1.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img))

###################################################
###################################################

#### Detecting Characters
hImg, wImg, _ = img.shape
# config = r'--oem 3 --psm 6 outputbase digits'
# boxes = pytesseract.image_to_boxes(img, config=config)  # boxes type --> str
boxes = pytesseract.image_to_boxes(img)  # boxes type --> str

# splitlines splits str into list items at every newline
for box in boxes.splitlines():
    b = box.split()
    # print(b)
    x1, y1, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    cv2.rectangle(img, (x1, hImg-y1), (x2, hImg-y2), (0, 0, 255), 1)
    cv2.putText(img, b[0], (x1, hImg-y1+25), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

###################################################
###################################################

# #### Detecting Words
# hImg, wImg, _ = img.shape
# boxes = pytesseract.image_to_data(img)  # boxes type --> str
#
# # splitlines splits str into list items at every newline
# for c, box in enumerate(boxes.splitlines()):
#     if c != 0:
#         b = box.split()
#         print(b)
#         if len(b) == 12:
#             x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
#             cv2.rectangle(img, (x, y), (w+x, h+y), (0, 0, 255), 1)
#             cv2.putText(img, b[11], (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

###################################################
###################################################

#### Detecting Numbers
# hImg, wImg, _ = img.shape
# config = r'--oem 3 --psm 6 outputbase digits'
# boxes = pytesseract.image_to_data(img, config=config)  # boxes type --> str
#
# # splitlines splits str into list items at every newline
# for c, box in enumerate(boxes.splitlines()):
#     if c != 0:
#         b = box.split()
#         print(b)
#         if len(b) == 12:
#             x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
#             cv2.rectangle(img, (x, y), (w+x, h+y), (0, 0, 255), 1)
#             cv2.putText(img, b[11], (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

cv2.imshow('Result', img)
cv2.waitKey(0)
