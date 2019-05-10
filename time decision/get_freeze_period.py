import cv2
import os
import sys

videoFolder="D:\\AIC2019\\aic19-track3-train-data\\"
output = "D:\\AIC2019\\frozen_frames_training.txt"
RGBDiffThresh = 3000
DiffAllowance = 10
MinFrames = 120

out = open(output,'w')
for i in range(1,101):
    print("vid%d\n"%(i))
    count = 1
    videoPath = videoFolder + "%d.mp4"%(i)
    cap = cv2.VideoCapture(videoPath)
    ret, frame2 = cap.read()
    start = -1
    consec = 0
    while(cap.isOpened()):
        frame1 = frame2
        ret, frame2 = cap.read()
        if(ret == True):
            count +=1
            difference = cv2.subtract(frame1, frame2)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) <= RGBDiffThresh and cv2.countNonZero(g) <= RGBDiffThresh and cv2.countNonZero(r) <= RGBDiffThresh:
                if(start == -1):
                    start = count - 1
                    consec = 0;
            elif(start != -1):
                consec += 1;
                if(consec > DiffAllowance):
                    if(count - start - consec > MinFrames):
                        print("vid %d: [%d,%d]\n"%(i,start, count-1-consec))
                        out.write("%d %d %d\n"%(i, start, count-1-consec));
                    start = -1
                    consec = 0
                    
        else:
            break
    if(start != - 1 and start != count -1):
        print("vid %d\n"%(i))
        start = - 1
out.close();
