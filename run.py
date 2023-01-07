import psutil
import time
from datetime import datetime

import cv2

def sketch(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask

cap = cv2.VideoCapture(0)
prev_frame_time = 0
new_frame_time = 0

if not cap.isOpened():
    print("Failed to launch camera")
    exit()
    
while True:
    ret, frame = cap.read()
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    # Get CPU and memory usage
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    FPS = "FPS : " + str(fps)
    DT = "Timestamp : " + str(datetime.now())
    CPU = "CPU usage : " + str(cpu_usage) + "%"
    MEM = "Memory usage : " + str(memory_usage) + "%"
    print("Console Log | ", DT, " | ", CPU, " | ", MEM, " | ", FPS)
    
    feed = sketch(frame)
    cv2.imshow('CAM FEED', feed)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
