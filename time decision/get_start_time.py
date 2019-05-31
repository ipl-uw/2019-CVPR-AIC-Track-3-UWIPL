import cv2
import os
import sys
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
 
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
 
    # return the intersection over union value
    return iou

stopTimePath = "D:\\AIC2019\\stop_time.txt"
enterGrassTime = "D:\\AIC2019\\enter_grass_time.txt"
backgroundStopTime = "D:\\AIC2019\\anomaly_candidate_processed2.txt"
outPath = "D:\\AIC2019\\anomaly_start_time.txt"
out = open(outPath,'w')
startTime = [100000]*100

# read stop times
with open(stopTimePath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
for k in range(len(content)):
    words = content[k].split(' ')
    if(startTime[int(words[0])-1] > int(words[1])):
        startTime[int(words[0])-1] = int(words[1])

# read enter grass times
with open(enterGrassTime) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
for k in range(len(content)):
    words = content[k].split(' ')
    # if enter grass time is less than anomaly start time, it becomes the new anomaly start time
    if(startTime[int(words[0])-1] > int(words[1])):
        startTime[int(words[0])-1] = int(words[1])

# read background stop time
with open(enterGrassTime) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
for k in range(len(content)):
    words = content[k].split(' ')
    # if background stop time is less than anomaly start time, it becomes the new anomaly start time
    if(startTime[int(words[0])-1] > int(words[1])):
        startTime[int(words[0])-1] = int(words[1])

for i in range(100):
    if(startTime[i] != 100000):
        print("%d %d %f\n"%(i+1, startTime[i], startTime[i]/30.0))
        out.write("%d %d %f\n"%(i+1, startTime[i], startTime[i]/30.0))
out.close()

        
