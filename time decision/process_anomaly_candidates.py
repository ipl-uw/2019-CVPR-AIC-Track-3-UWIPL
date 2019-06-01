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
    iou = float(interArea) / float(boxAArea + boxBArea - interArea)
 
    # return the intersection over union value
    return iou

# assumes fps for anomalyCandidate.txt is 5 and fps for frozen_frames.txt is 30
# outputs in 30 fps
anomalyCandidatePath = "/home/xinyu/yolo/darknet/data/track3_test_bg_detection_V3/Script/anomalyCandidate.txt"
detectionPath= "/home/xinyu/yolo/darknet/data/track3_test_bg_detection_V3/"
outfile="anomalyCandidate_processed.txt"
frozenframesPath="frozen_frames.txt"
fps = 5

with open(anomalyCandidatePath) as f:
    content = f.readlines()
content = [x.strip('\n') for x in content]
out = open(outfile,'w')
iou = 0.0
with open(frozenframesPath) as f:
    content2 = f.readlines()
for i in range(len(content)):
    words = content[i].split(' ')
    boxA = [int(words[4]), int(words[6]), int(words[5]), int(words[7])]
    ignore = 0
    for n in range(len(content2)):
	words3 = content2[n].split(' ');
	if(int(words3[1])<=(int(words[1])+50)*30/fps and int(words3[2])>=int(words[1])*30/fps and words3[0]==words[0]):
	    ignore = 1
    if(ignore == 0):
	    for j in range(min(8*fps,int(words[1])+1), int(words[1])+5):
		backgroundDetPath = detectionPath + words[0] + '/' + 'vid' + words[0] + '_' + str(j) + '.txt'
		with open(backgroundDetPath) as g:
		    lines = g.readlines()
		lines = [x.strip('\n') for x in lines]
		iou = 0
		for k in range(len(lines)):
		    words2 = lines[k].split(' ')
		    boxB = [int(words2[2]), int(words2[4]), int(words2[3]), int(words2[5])]
		    iou = bb_intersection_over_union(boxA, boxB)
		    if(iou>0.05):		
			for n in range(len(content2)):
			    words3 = content2[n].split(' ');
			    if(int(words3[0])>int(words[0])):
				break;
			if(ignore<1):
			    print(iou)
		            out.write("%s %d %s\n"%(words[0], j*6, lines[k]))
		        break
		if(iou > 0.05):
		    break
            
    
