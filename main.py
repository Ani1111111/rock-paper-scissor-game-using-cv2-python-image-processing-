from handDetector import HandDetector
import cv2
import math
import time
import random
import numpy as np


handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)
TIMER = int(20)
t=3


while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count=0

    if(len(handLandmarks) != 0):
        #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        #details: https://google.github.io/mediapipe/solutions/hands

        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
            count = count+1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
            count = count+1
        if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
            count = count+1
        if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
            count = count+1
        if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
            count = count+1
        if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
            count = count+1
    p = cv2.imread('paper.jfif')
    st = cv2.imread('stone.jfif')
    sc = cv2.imread('scissor.jfif')
    l = ['p','st','sc']
    ch = random.choice(l)
    if ch=='p':
        s_img = p
    elif ch=='st':
        s_img = st
    else:
        s_img =sc
    x_offset=y_offset=50
    image[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
    # s_img = cv2.imread("paper.jfif", -1)

    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]

    alpha_s = s_img[:, :, 2] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        image[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                              alpha_l * image[y1:y2, x1:x2, c])
    cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
    cv2.putText(image,'press q to start' , (45, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Game", image)
    k = cv2.waitKey(1)
    if k == ord('q'):
        cv2.destroyAllWindows()
        cv2.imshow('image',image)
        if (count ==5 and ch=='st') or (count==2 and ch =='p') or (count==0 and ch =='sc'):
            img = np.zeros([512,512,3],np.uint8)#it create a black image
            cv2.putText(img,'you win' , (100, 320), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
            cv2.imshow('result',img)
        elif (count ==5 and ch=='p') or (count==2 and ch =='sc') or (count==0 and ch=='st'):
            pass
        else:
            img = np.zeros([512,512,3],np.uint8)#it create a black image
            cv2.putText(img,'you lose' , (100, 320), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
            cv2.imshow('result',img)
        cv2.waitKey(0)
        
 
    # Press Esc to exit
    elif k == 27:
        break


webcamFeed.release()
cv2.destroyAllWindows()
    