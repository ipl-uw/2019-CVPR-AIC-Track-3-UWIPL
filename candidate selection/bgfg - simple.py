import cv2
import os
import numpy as np

rt = './data/aic19-track3-train-data'
videos = os.listdir(rt)
wrt_ori = './data/frames' # original frames
wrt_bg = './data/bg-train' # background for each frame
wrt_fgmask = './data/mask-train' # traffic flow mask for each video
wrt_bgvideo = './data/bg/video-train'
# if not os.path.exists(wrt_ori):
#     os.mkdir(wrt_ori)
# if not os.path.exists(wrt_bg):
#     os.mkdir(wrt_bg)
# if not os.path.exists(wrt_fgmask):
#     os.mkdir(wrt_fgmask)
if not os.path.exists(wrt_bgvideo):
    os.mkdir(wrt_bgvideo)

for video in videos:
    out = 0
    print (video)
    if not os.path.exists(os.path.join(wrt_bg, video.split('.')[0])):
        os.mkdir(os.path.join(wrt_bg, video.split('.')[0]))
    if not os.path.exists(os.path.join(wrt_ori, video.split('.')[0])):
        os.mkdir(os.path.join(wrt_ori, video.split('.')[0]))

    #read video
    cap = cv2.VideoCapture(os.path.join(rt, video))
    ret, frame = cap.read()
    # extract background with MOG
    # you can change the history to see the output, 120 seems to be good for most cameras
    bs = cv2.createBackgroundSubtractorMOG2(history=120)
    bs.setHistory(120)
    bgvideo = os.path.join(wrt_bgvideo, str(int(video.split('.')[0])).zfill(1) + '.avi')
    videoWriter = cv2.VideoWriter(bgvideo, cv2.VideoWriter_fourcc(*'XVID'), 30, (800, 410))
    count = 1
    while ret:
        fg_mask = bs.apply(frame)
        bg_img = bs.getBackgroundImage()

        fg = cv2.subtract(frame,bg_img)
        fg = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)
        out = cv2.bitwise_or(out,fg)
        out = cv2.medianBlur(out, 3) # Clear the image, remove small spots
        out = cv2.GaussianBlur(out, (3, 3), 0) # Smooth the image

        # remove abnormal trajectory
        ret, out = cv2.threshold(out, 10, 255, cv2.THRESH_TOZERO)
        ret, out = cv2.threshold(out, 110, 255, cv2.THRESH_BINARY)
        # visualization of generating mask
        # cv2.imshow("out", out)
        # cv2.waitKey(1)
        #if count > 500:
            #cv2.imwrite(os.path.join(wrt_bg, video.split('.')[0], str(int(count)).zfill(3)+'.jpg'), bg_img)
        videoWriter.write(bg_img)
        #cv2.imwrite(os.path.join(wrt_bg, video.split('.')[0], str(int(count)).zfill(3) + '.jpg'), bg_img)
        #cv2.imwrite(os.path.join(wrt_ori, video.split('.')[0], str(int(count)).zfill(3)+'.jpg'), frame)
        ret, frame = cap.read()
        count += 1
        #if count == 600:
        #    break
    # edges = cv2.Canny(out, 200, 200)
    # lines = cv2.HoughLines(edges, 3, np.pi / 180, 200)
    cv2.imwrite(os.path.join(wrt_fgmask, str(int(video.split('.')[0])).zfill(3) + '.jpg'), out)


