import time
import cv2

vpath = "/Users/aalobaid/Downloads/Tuber/Tuber/idlenormal.mp4"


while True:
    cap = cv2.VideoCapture(vpath)
    time.sleep(0.1)
    print("Another")