# This script convert YOLO detection result from original anomaly candidate video
# to MOT format for TNT to read

import os

rt = './YOLO Results'
wrt = './MOT'
name = os.listdir(rt)
for n in name:
	g = open(os.path.join(wrt, str(n) + '.txt'), 'w')
	f = os.listdir(os.path.join(rt, n))
	#print(f)
	for j in range(1, len(f)+1):

		with open(os.path.join(rt, n, 'vid'+str(n)+'_'+str(j)+'.txt')) as f:
			content = f.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
		content = [x.strip('\n') for x in content]
		for i in range(len(content)):
			print('n=' + n + 'j=' + str(j) + 'i=' + str(i))
			words = content[i].split(' ')
			output = "%d, -1, %s, %s, %d, %d, %f, -1, -1, -1\n"%( j, words[2], words[4],  int(words[3])-int(words[2]), int(words[5])-int(words[4]), float(words[1]))
			g.write(output)

	g.close()
