import cv2
import os
import sys
stopTimePath = outPath = "D:\\AIC2019\\stop_time.txt"
SCTPath = "D:\\AIC2019\\yolo_txt_result_processed\\"
maskPath = "D:\\AIC2019\\aic19-track3-frames-svm-k4-fill\\"
with open(stopTimePath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
for i in range(len(content)):
    words = content[i].split(' ')
    vid=int(words[0])
    TrackingPath = SCTPath + "%0.2d_%d.txt"%(vid, int(float(words[1])/30.0/180.0)+1)
    mask = cv2.imread(maskPath + "\\%0.3d-grass-mask-fill.png"%(vid),cv2.IMREAD_GRAYSCALE)
    with open(TrackingPath) as g:
        content2 = g.readlines()
    content2 = [x.strip('\n') for x in content2]
    inGrassID=[]
    for j in range(len(content2)):
        words2 = content2[j].split(',')
        if(int(words2[0]) >=  int(words[1])/3-300 and int(words2[0]) < int(words[1])/3 and words2[1] not in inGrassID):
            x1 = int(words2[2])
            x2 = int(words2[2])+int(words2[4])
            y1 = int(words2[3])
            y2 = int(words2[3])+int(words2[5])
            width = int(words2[4])
            height = int(words2[5])
            pixVal = 0
            for h in range(y1+int(0.75*height), y2):
                for w in range(x1,x2):
                    pixVal+=mask[h,w]
            pixVal=pixVal/(0.25*height*width)
            if(pixVal>200):
                inGrassID.append(words2[1])
    print(inGrassID)
    for ID in inGrassID:
        consec = 0
        start = 0
        for j in range(len(content2)):
            words2 = content2[j].split(',')
            if(int(words2[0]) >=  int(words[1])/3-300 and int(words2[0]) < int(words[1])/3 and words2[1] == ID):
                x1 = int(words2[2])
                x2 = int(words2[2])+int(words2[4])
                y1 = int(words2[3])
                y2 = int(words2[3])+int(words2[5])
                width = int(words2[4])
                height = int(words2[5])
                pixVal = 0
                for h in range(y1+int(0.5*height), y2):
                    for w in range(x1,x2):
                        pixVal+=mask[h,w]
                pixVal=pixVal/(0.5*height*width)
                if(pixVal>240 and width*height>300):
                    consec +=1
                    if(start ==0):
                        start = int(words2[0])
        if(consec>=5):
            print("Vid %d ID %d frame %d consec %d\n"%(int(vid), int(ID), start, consec))
