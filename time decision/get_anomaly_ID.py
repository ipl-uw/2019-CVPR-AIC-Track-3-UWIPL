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

anomalyCandidatePath = "D:\\AIC2019\\anomalyCandidate_processed.txt"
anomalyCandidatePath2 = "D:\\AIC2019\\anomalyCandidate_processed2.txt"
SCTPath = "D:\\AIC2019\\yolo_txt_result_processed\\"
outPath = "D:\\AIC2019\\anomaly_candidate_ID_temp.txt"
outPath2="D:\\AIC2019\\anomaly_candidate_ID.txt"
outPath3 = "D:\\AIC2019\\anomaly_candidate_NoID.txt"
maskPath = "D:\\AIC2019\\mask"
trajectoryOutPath = "D:\\AIC2019\\anomaly_candidate_trajectory\\"


#get anomaly candidates
with open(anomalyCandidatePath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
part = 0
out = open(outPath,'w')
out2 = open(outPath3, 'w')
IOUThresh = 0.4

dellist=[]

#apply mask to eliminate false positives
margin = 5
for i in  range(len(content)):
    words = content[i].split(' ')
    mask = cv2.imread(maskPath + "\\%0.3d.jpg"%(int(words[0])),cv2.IMREAD_GRAYSCALE)
    color = cv2.imread(maskPath + "\\%0.3d.jpg"%(int(words[0])))
    if(int(words[1]) < 600):
        x1 = int(words[4]) -margin
        x2 = int(words[5]) +margin
        y1 = int(words[6]) -margin
        y2 = int(words[7]) +margin
        cv2.rectangle(color,(x1, y1), (x2, y2), (0,255,0), 3)
        count = 0;
        if(y1 > 410):
            y1 = "410"
        if(y2 > 410):
            y2 = "410"
        if(x1 > 800):
            x1 = "800"
        if(x2 > 800):
            x2 = "800"
        if(int(mask[y1-1,x1-1]) < 200):
            count+=1
        if(int(mask[y1-1,x2-1]) < 200):
            count+=1
        if(int(mask[y2-1,x1-1]) < 200):
            count+=1
        if(int(mask[y2-1,x2-1]) < 200):
            count+=1
        if(count >= 4):
            dellist.append(i)
            #print(words)
            #crop = mask[y1:y2, x1:x2]
            #cv2.imshow('image',color)
            #cv2.waitKey(0)

# delete false positives from anomaly candidates
for i in range(len(dellist)):
    del content[dellist[len(dellist)-1-i]]

# output new anomaly candidate list
newAnomalyList = open(anomalyCandidatePath2,'w')
for i in  range(len(content)):
    newAnomalyList.write(content[i]+"\n")
newAnomalyList.close()

# get ID for anomaly candidates
timeframe = 80
for k in range(len(content)):
    words = content[k].split(' ')
    frame = int(words[1])
    
    # since videos are split into 5 parts for SCT, we get the part number corresponding to the frame
    if(frame >150):
        if(frame < 210*30):
            TrackingPath = SCTPath + "%0.2d_1.txt"%(int(words[0]))
            part = 1
        elif(frame < 210*30+180*30):
            TrackingPath = SCTPath + "%0.2d_2.txt"%(int(words[0]))
            part = 2
        elif(frame < 210*30+180*30*2):
            TrackingPath = SCTPath + "%0.2d_3.txt"%(int(words[0]))
            part = 3
        elif(frame < 210*30+180*30*3):
            TrackingPath = SCTPath + "%0.2d_4.txt"%(int(words[0]))
            part = 4
        else:
            TrackingPath = SCTPath + "%0.2d_5.txt"%(int(words[0]))
            part = 5
            
        # get corresponding SCT part frame number
        frame2 = int((frame-(part-1)*180*30)/3)
        #print(TrackingPath)
        boxA = [int(words[4]), int(words[6]), int(words[5]), int(words[7])]
        with open(TrackingPath) as g:
            lines = g.readlines()
        lines = [x.strip('\n') for x in lines]
        for i in range(len(lines)):
            words2 = lines[i].split(',')

            # search SCT results for corresponding trajectory ID within 80 frames (10 fps) of when anomaly candidates appear in background
            if(int(words2[0]) <= frame2 and int(words2[0]) > frame2 - timeframe):
                boxB=[int(words2[2]), int(words2[3]), int(words2[2])+int(words2[4]), int(words2[3])+int(words2[5])]
                if(bb_intersection_over_union(boxA, boxB) > IOUThresh):
                    out.write("%d %d %d %d %d %d %d\n"%(int(words[0]), part, int(words2[1]), int(words[4]), int(words[5]), int(words[6]), int(words[7])))
                    print("video %d car id %d"%(int(words[0]), int(words2[1])))
                    break
        if(bb_intersection_over_union(boxA, boxB) <= IOUThresh):
            out2.write("%s\n"%(content[k]))
out.close()
out2.close()

# Check if trajectory starts in previous part
with open(outPath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
part = 0
out = open(outPath2, "w")

# loop through temp IDs
for k in range(len(content)):
    loop = 1
    words = content[k].split(' ')
    TrackingPath = SCTPath + "%0.2d_%d.txt"%(int(words[0]), int(words[1]))
    part = int(words[1])
    
    with open(TrackingPath) as g:
        lines = g.readlines()
    lines = [x.strip('\n') for x in lines]
    
    boxA=[int(words[3]), int(words[5]), int(words[4]), int(words[6])]

    for i in range(len(lines)):
        words2 = lines[i].split(',')
        boxB=[int(words2[2]), int(words2[3]), int(words2[2])+int(words2[4]), int(words2[3])+int(words2[5])]
        iou = 0
        if(words2[1] == words[2]):
            # if trajectory starts at beginning of part, check previous part
            if(int(words2[0]) < 20):
                if(part>1):
                    part-=1
                    TrackingPath = SCTPath + "%0.2d_%d.txt"%(int(words[0]), part)
                    with open(TrackingPath) as h:
                        lines2 = h.readlines()
                    lines2 = [x.strip('\n') for x in lines2]
                    for j in range(len(lines2)):
                        words3 = lines2[j].split(',')
                        if(int(words3[0]) > int(lines2[len(lines2)-1].split(',')[0])-5):
                            #print(words3)
                            boxB=[int(words3[2]), int(words3[3]), int(words3[2])+int(words3[4]), int(words3[3])+int(words3[5])]
                            iou = bb_intersection_over_union(boxA, boxB)
                            if(iou > IOUThresh):
                                #print(words3)
                                out.write("%d %d %d\n"%(int(words[0]), part, int(words3[1])))
                                break
                if(iou > IOUThresh):
                    break
            # if trajectory does not start at beginning of part, keep current ID
            out.write("%d %d %d\n"%(int(words[0]), part, int(words2[1])))
            break
out.close()

# output anomaly trajectories
with open(outPath2) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]

for i in range(len(content)):
    words = content[i].split(' ')
    TrackingPath = SCTPath + "%0.2d_%d.txt"%(int(words[0]), int(words[1]))
    out=open(trajectoryOutPath + "%0.2d_%s_%s.csv"%(int(words[0]), words[1], words[2]), 'w')
    with open(TrackingPath) as g:
        lines = g.readlines()
    lines = [x.strip('\n') for x in lines]
    for j in range(len(lines)):
        words2 = lines[j].split(',')
        if(words[2] == words2[1]):
            out.write("%s,%s,%s\n"%(words2[0],words2[2],words2[3]))
    out.close()
