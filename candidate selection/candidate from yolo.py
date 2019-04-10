import os
# result is a list of two parameters [type, continue_num]
# iterate every folder -- 1 folder represent 1 video result

def iteration(path, num):
    previous_Type = None
    COUNT_LIST = []
    count = 0
    Type = False  # False means negative type
    # directory for yolo background detection result
    path = '/home/xinyu/yolo/darknet/data/track3_test_bg_detection/'
    Len = os.listdir(os.path.join(path, str(num)))

    for k in range(1, len(Len)):
        # for file in files:
        filename = path + str(num) + '/vid' + str(num) + '_' + str(k) + '.txt'
        # filename = path + '/' + file
        file = open(filename, 'r')
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
            else:
                if previous_Type == 0:
                    COUNT_LIST.append('undetected ' + str(count))
                else:
                    COUNT_LIST.append('detected ' + str(count))
                    if count >= 1800:  # when detected condition over 1 min, record the video type as positive
                        Type = True
                count = 1
                previous_Type = current_Type
        file.close()
    if previous_Type == 0:
        COUNT_LIST.append('undetected ' + str(count))
    else:
        COUNT_LIST.append('detected ' + str(count))
        if count >= 1800:  # when detected condition over 1 min, record the video type as positive
            Type = True
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