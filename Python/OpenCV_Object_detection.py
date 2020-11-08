import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import time

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
        
    img_name = "opencv_frame.png"
    cv2.imwrite(img_name, frame)
    # cv2.imshow("test", frame)
    im = cv2.imread(img_name)
    bbox, label, conf = cv.detect_common_objects(im, confidence=0.5, enable_gpu=True)
    output_image = draw_bbox(im, bbox, label, conf)
    cv2.imshow("test" ,output_image)
    time.sleep(2)


cam.release()

cv2.destroyAllWindows()