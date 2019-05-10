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
SCTPath = "D:\\AIC2019\\yolo_txt_result_processed\\"
outPath = "D:\\AIC2019\\anomaly_candidate_ID_temp.txt"
outPath3 = "D:\\AIC2019\\anomaly_candidate_NoID.txt"
video = ' '
with open(anomalyCandidatePath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
part = 0
out = open(outPath,'w')
out2 = open(outPath3, 'w')
for k in range(len(content)):
    words = content[k].split(' ')
    frame = int(words[1])
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
        frame2 = int((frame-(part-1)*180*30)/3)
        print(TrackingPath)
        boxA = [int(words[4]), int(words[6]), int(words[5]), int(words[7])]
        with open(TrackingPath) as g:
            lines = g.readlines()
        lines = [x.strip('\n') for x in lines]
        for i in range(len(lines)):
            words2 = lines[i].split(',')
            if(int(words2[0]) <= frame2 and int(words2[0]) > frame2 -80):
                boxB=[int(words2[2]), int(words2[3]), int(words2[2])+int(words2[4]), int(words2[3])+int(words2[5])]
                if(bb_intersection_over_union(boxA, boxB) > 0.4):
                    out.write("%d %d %d %d %d %d %d\n"%(int(words[0]), part, int(words2[1]), int(words[4]), int(words[5]), int(words[6]), int(words[7])))
                    print("video %d car id %d"%(int(words[0]), int(words2[1])))
                    break
        if(bb_intersection_over_union(boxA, boxB) <= 0.4):
            out2.write("%s\n"%(content[k]))
out.close()
out2.close()
with open(outPath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
part = 0
outPath2="D:\\AIC2019\\anomaly_candidate_ID.txt"
out = open(outPath2, "w")
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
                            print(words3)
                            boxB=[int(words3[2]), int(words3[3]), int(words3[2])+int(words3[4]), int(words3[3])+int(words3[5])]
                            iou = bb_intersection_over_union(boxA, boxB)
                            if(iou > 0.4):
                                print(words3)
                                out.write("%d %d %d\n"%(int(words[0]), part, int(words3[1])))
                                break
                if(iou > 0.4):
                    break
            out.write("%d %d %d\n"%(int(words[0]), part, int(words2[1])))
            break
out.close()
