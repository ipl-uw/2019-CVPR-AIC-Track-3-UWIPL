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

# Path to Single Camera Tracking Results
SCTPath = "D:\\AIC2019\\yolo_txt_result\\"
outFolder ="D:\\AIC2019\\yolo_txt_result_processed\\"
IOUThesh = 0.6
frameRange = 20
for m in range(1,101):
    for n in range(1,6):  
        TrackingPath = SCTPath + "%0.2d_%d.txt"%(m,n)
        outPath = outFolder + "%0.2d_%d.txt"%(m,n)
        match = []
        matchFound = 0;
        lastindex=0;
        lastframe = 0;
        with open(TrackingPath) as f:
            content = f.readlines()
        content = [x.strip('\n') for x in content]
        tested = []
        for i in range(len(content)):
            words = content[i].split(',')
            ignore=[]
            framelist=[]
            if(words[1] not in tested):
                for j in range (i, len(content)):
                    words2 = content[j].split(',')
                    if(words2[1] == words[1]):
                        lastframe = int(words2[0])
                        lastindex = j
                        boxA=[int(words2[2]), int(words2[3]), int(words2[2])+int(words2[4]), int(words2[3])+int(words2[5])]
                tested.append(words[1])
                for j in range (lastindex, len(content)):
                    words2 = content[j].split(',')
                    if(words[1] == words2[1]):
                        if(words2[0] not in framelist):
                            framelist.append(words2[0])
                for j in range (lastindex, len(content)):
                    words2 = content[j].split(',')
                    if(words2[0] in framelist):
                        if(words2[1] not in ignore):
                            ignore.append(words2[1])
                for j in range (lastindex, len(content)):
                    words2 = content[j].split(',')
                    if(int(words2[0])-lastframe > frameRange):
                        break
                    if(int(words2[0]) > lastframe and (words2[1] not in ignore) ):
                        boxB=[int(words2[2]), int(words2[3]), int(words2[2])+int(words2[4]), int(words2[3])+int(words2[5])]
                        if(bb_intersection_over_union(boxA, boxB) > IOUThesh):
                            temp = [int(words[1]), int(words2[1])]
                            if(temp not in match):
                                match.append(temp)
                            else:
                                break
        print(str(m)+"_"+str(n))
        print(match)
        for pair in reversed(match):
            for i in range(len(content)):
                words = content[i].split(',')
                if(int(words[1]) == pair[1]):
                    words[1] = str(pair[0])
                    content[i] = "%s,%s,%s,%s,%s,%s,%s,%s,%s"%(words[0],words[1],words[2],words[3],words[4],words[5],words[6],words[7],words[8])
        out = open(outPath,"w")
        for i in range(len(content)):
            out.write(content[i]+"\n")
        out.close()
