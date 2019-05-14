import cv2
import os
import numpy as np

rt = './data/bg/26'
mask_fd = './data/mask/'
backgrounds = os.listdir(rt)
mask = cv2.imread(os.path.join(mask_fd,'26.jpg'),cv2.IMREAD_GRAYSCALE)[10:100,0:800]

out = 0
b = 0

for i in range(500, len(backgrounds), 10):
    if i + 1000 < len(backgrounds):
        print(backgrounds[i+1000] + ' - ' + backgrounds[i])
        pic_1 = cv2.imread(os.path.join(rt, backgrounds[i]))[10:100,0:800]
        pic_2 = cv2.imread(os.path.join(rt, backgrounds[i + 1000]))[10:100,0:800]
        sub = cv2.subtract(pic_2, pic_1)
        sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
        sub = cv2.medianBlur(sub, 3)
        #ret, out = cv2.threshold(sub, 30, 255, cv2.THRESH_TOZERO)
        ret, out = cv2.threshold(sub, 20, 255, cv2.THRESH_BINARY)
        a = np.argmax(out, axis=1)
        b = np.argmax(a)
        ret, out = cv2.threshold(sub, 17*b - 317, 255, cv2.THRESH_BINARY)
        # print(out.shape, mask.shape)
        out = cv2.bitwise_and(out, mask)
        #out = cv2.medianBlur(out, 3)
        print(np.sum(out))
        # print((i + 1000) / 30)
        cv2.imshow("out", out)
        cv2.waitKey(10)
        if np.sum(out) > 512:
            print(np.sum(out))
            cv2.imshow("out", out)
            cv2.waitKey(0)
            print((i+150)/30)
            break


# cv2.imshow("out", out)
# cv2.waitKey(0)







