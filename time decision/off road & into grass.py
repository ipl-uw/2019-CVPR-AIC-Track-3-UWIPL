# This script is used to generate demo video.
# Can be simply modified to get the starting time for cases of go off the road
import cv2

cap = cv2.VideoCapture("accident_detection.avi")
ret, frame = cap.read()
count = 1
road = cv2.imread("mask.jpg")
#road = cv2.bitwise_not(road)

road[:, :, 2] = 255
#cv2.imshow("out", road)
#cv2.waitKey(0)


while ret:
    out = cv2.addWeighted(frame, 1, road, 0.2, 0)
    cv2.imshow("out", out)
    cv2.waitKey(20)
    end = frame
    ret, frame = cap.read()
    count += 1

#cv2.imwrite("road.jpg",end)
