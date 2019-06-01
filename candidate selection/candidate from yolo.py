import os
# result is a list of two parameters [type, continue_num]
# iterate every folder -- 1 folder represent 1 video result

def iteration(path, num):
previous_Type = None
    COUNT_LIST = []
    count = 0
    Type = False # False means negative type
    path = '/home/xinyu/yolo/darknet/data/track3_test_bg_detection_V3/'
    Len = os.listdir(os.path.join(path,str(num)))
    output = 0
    outfile = open(path+'Script/anomalyCandidate.txt','a+')
    consec = 0
    fps = 5    # change fps to match video fps
    for k in range(1, len(Len)):
    #for file in files:
        filename = path + str(num) + '/vid' + str(num) + '_' + str(k) + '.txt'
        # filename = path + '/' + file
        file = open(filename,  'r')
        # print(filename)
        # set 0 for empty content type, 1 for the others
        current_Type = None
        if os.stat(filename).st_size == 0:
            current_Type = 0
        else:
            current_Type = 1
        # first file
        if previous_Type == None:
            previous_Type = current_Type
            count += 1
        # all the other files
        else:
            # if continuous

            if previous_Type == current_Type:
                count += 1
            # if change condition, store the type and count number into list of list
            # update the count value to zero and update the type value
	    elif consec<3*fps and count <60*fps:
		consec+=1
            else:
		consec = 0
                if previous_Type == 0:
                    COUNT_LIST.append('undetected '+ str(count + consec))
                else:
                    COUNT_LIST.append('detected ' + str(count + consec))
                    if (count >= 60*fps) or (count >=40*fps and k < 60*fps and count >= k-8*fps): # when detected condition over 1 min, record the video type as positive
			if output == 0:
			    COUNT_LIST.append('first frame ' + str(max(k-count,8*fps)))
			    output = 1
			    tempfile = path + str(num) + '/vid' + str(num) + '_' + str(max(k-count+1,8*fps)) + '.txt'
			    framenum=max(k-count+1,8*fps)+1;
			    loop = 0
			    while(loop==0):
				tempfile = path + str(num) + '/vid' + str(num) + '_' + str(framenum) + '.txt'
			        with open(tempfile) as f:
    				    content = f.readlines()
				framenum+=1
				loop = len(content)
			    for i in range(len(content)):
				if(len(content)<8):
			    	    outfile.write(str(num)+' '+str(max(k-count+1,8*fps))+ ' '+content[i])
                        Type = True
                count = 1
                previous_Type = current_Type
        file.close()
    if previous_Type == 0:
        COUNT_LIST.append('undetected ' + str(count+consec))
    else:
        COUNT_LIST.append('detected ' + str(count+consec))
        if count >= 60*fps or (count >=40*fps and k < 40*fps and count >= k-8*fps):  # when detected condition over 1 min, record the video type as positive
	    COUNT_LIST.append('first frame ' + str(max(k-count,8*fps)))
	    output = 1
	    tempfile = path + str(num) + '/vid' + str(num) + '_' + str(max(k-count+1,8*fps)) + '.txt'
	    framenum=max(k-count+1,8*fps)+1;
	    loop = 0
	    while(loop==0):
		tempfile = path + str(num) + '/vid' + str(num) + '_' + str(framenum) + '.txt'
	        with open(tempfile) as f:
    		    content = f.readlines()
		framenum+=1
		loop = len(content)
	    for i in range(len(content)):
		if(len(content)<8):
	    	    outfile.write(str(num)+' '+str(max(k-count+1,8*fps))+ ' '+content[i])
            Type = True
    outfile.close()
    return [COUNT_LIST, Type]


# save detailed result for each video
for i in range(100, 101):

    #print('a new iteration is start\n')
    COUNT_LIST = []
    path = '/home/xinyu/yolo/darknet/data/track3_test_bg_detection/'
    [COUNT_LIST, Type] = iteration(path, i)
    f = open('num_result' + str(i) + '.txt', "w")
    # negative means anomaly case, otherwise positive
    if Type is True:
        f.write('positive\n')
        f.write('This is an anomaly candidate, positive\n')
    else:
        f.write('negative\n')
        f.write('This is not an anomaly candidate, nigative\n')
    for item in COUNT_LIST:
        f.write(item+'\n')
        #print(item)
    f.close()
    print('The iteration ' + str(i) + ' is end\n')

# save all the result to a summary file containing all the candidates
result = []
for i in range(1, 101):
    path = '/home/xinyu/yolo/darknet/data/track3_test_bg_detection/script/'
    f = open(path + 'num_result' + str(i) + '.txt', "r")
    first_line = f.readline()
    result.append(first_line)
    f.close()
f = open('result_summary.txt', 'w')
for i in range(1, 101):
    f.write(str(i) + ' ' + result[i-1])
f.close()
print('end')
