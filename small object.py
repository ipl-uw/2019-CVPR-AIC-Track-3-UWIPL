import cv2
import os
import numpy as np
import math

# bg images are saved under rt, change it if you want to read all 100 videos
rt = './data/bg/26'
backgrounds = os.listdir(rt)
# read generated mask, change it if you want to read all 100 videos
img = cv2.imread("26_mask.jpg")

# getting two line with the biggest and smallest k
# First get the edge and all the possible lines
edges = cv2.Canny(img, 200, 200)
lines = cv2.HoughLines(edges, 3, np.pi / 180, 200)
# get the line with minimum and maximum k
max = -9999
min = 0
for line in lines:
    line = line[0]
    rho = line[0]
    theta = line[1]
    a = math.cos(theta)  # Calculate orientation in order to print them
    b = math.sin(theta)
    p0 = a * rho
    q0 = b * rho
    x0 = int(round(p0 + 1000 * (-b)))
    y0 = int(round(q0 + 1000 * (a)))
    x1 = int(round(p0 - 1000 * (-b)))
    y1 = int(round(q0 - 1000 * (a)))
    pt1 = (x0, y0)
    pt2 = (x1, y1)
    k =(y1 - y0)/(x1 - x0)
    if  k > 0:
        continue
    if k < min:
        min = k
        pt1_min = pt1
        pt2_min = pt2
    if k > max:
        max = k
        pt1_max = pt1
        pt2_max = pt2
#print(max,min)
# get the coordinate for intersection point
b_min = pt1_min[1] - min * pt1_min[0]
b_max = pt1_max[1] - max * pt1_max[0]
x_cross = (b_max - b_min)/(min - max)
#print(x_cross)
y_cross1 = min * x_cross + b_min
y_cross2 = max * x_cross + b_max
#print(y_cross1,y_cross2)

# Visualize ROI area, please write function searching for write spot if you want the generate the candidates
out = 0
for i in range(1000, len(backgrounds), 10):
    if i + 1000 < len(backgrounds):
        print(backgrounds[i+1000] + ' - ' + backgrounds[i])
        pic_1 = cv2.imread(os.path.join(rt, backgrounds[i]))[(int(round(y_cross1)) + 10):(int(round(y_cross1)) + 110),
                (int(round(x_cross) - 220)):(int(round(x_cross) - 20))]
        pic_2 = cv2.imread(os.path.join(rt, backgrounds[i + 800]))[(int(round(y_cross1)) + 10):(int(round(y_cross1)) + 110),
                (int(round(x_cross) - 220)):(int(round(x_cross) - 20))]
        sub = cv2.subtract(pic_2, pic_1)
        sub = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
        sub = cv2.medianBlur(sub, 3)
        #ret, out = cv2.threshold(sub, 30, 255, cv2.THRESH_TOZERO)
        ret, out = cv2.threshold(sub, 30, 255, cv2.THRESH_BINARY)
        #out = cv2.medianBlur(out, 3)
        cv2.imshow("out", out)
        cv2.waitKey(80)

cv2.imshow("out", out)
cv2.waitKey(0)







