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

anomalyIDPath = "D:\\AIC2019\\anomaly_candidate_curvefit.txt"
SCTPath = "D:\\AIC2019\\yolo_txt_result_processed\\"
video = ' '
outPath = "D:\\AIC2019\\stop_time.txt"
out = open(outPath,'w')
IOUThresh = [0.9, 0.8, 0.7]
frameSkip=[20, 15, 10]
consecFramesOverThresh = 1
stop = [-1]*100

with open(anomalyIDPath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]

for k in range(len(content)):
    trackList = []
    count = 0
    start = 1000000
    consec = 0
    words = content[k].split(' ')
    TrackingPath = SCTPath + "%0.2d_%d.txt"%(int(words[0]), int(words[1]))
    with open(TrackingPath) as g:
        lines = g.readlines()
    lines = [x.strip('\n') for x in lines]
    for i in range(len(lines)):
        words2 = lines[i].split(',')

        # if frame is after slowing down time or slowing down time is greater than 30s after trajectory start
        if(words2[1] == words[2] and (int(words2[0])>int(words[3]) or int(words[3])-min(start,int(words2[0])) > 300)):
            start = min(start, int(words2[0]))
            # add bbox at frame to trackList
            temp = [int(words2[2]), int(words2[3]), int(words2[2])+int(words2[4]), int(words2[3])+int(words2[5])]
            trackList.append(temp)
            count+=1

    # start with tighter threshold and if not stop time is obtained, use looser threshold       
    for j in range(0,3):
        for i in range(count-frameSkip[j]):

            # check if IOU of bbox at frame i and i+ frameSkip is greater than threshold
            if(bb_intersection_over_union(trackList[i], trackList[i+frameSkip[j]]) > IOUThresh[j]):
                consec+=1
            else:
                consec=0

            # if IOU is greater than threshold for a number of frames greater than the consecutive threshold
            if(consec>=consecFramesOverThresh):
                if(stop[int(words[0])-1]>(start - consec + 1 + i + (int(words[1])-1)*180*10)*3 or stop[int(words[0])-1] == -1):
                    stop[int(words[0])-1] = (start - consec + 1 + i + (int(words[1])-1)*180*10)*3
                print("%d %f"%(int(words[0]), float((start - consec + 1 + i + (float(words[1])-1)*180*10)/10.0)))
                break
        if(consec>=consecFramesOverThresh):
            break
#print(stop)
for i in range(100):
    if(stop[i] != -1):
        out.write("%d %d %f\n"%(i+1, stop[i], stop[i]/30.0))
out.close()

        
