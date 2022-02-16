# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

vid = cv2.VideoCapture('file_example_MP4_1280_10MG.mp4') #  replace 'rocket.mp4' with 0 for webcam
fps,st,frames_to_count,cnt = (0,0,20,0)

startTime = time.time()
frameCount = 0

while(vid.isOpened()):
    ret, frame = vid.read()
    if (ret):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Video Out", frame)
        frameCount += 1
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    else:
        break

endTime = time.time()
timeElapsed = endTime - startTime

print("There was a total of ", str(frameCount), "frames, rendered in ", str(timeElapsed), " seconds")
print("FPS: ", str(frameCount/timeElapsed))