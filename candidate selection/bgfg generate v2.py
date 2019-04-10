import cv2
import os
import numpy as np
import argparse
import uuid
import scipy.spatial

# Read the list of camera folders
with open("./list_cam.txt", "r") as f:
    vpath = f.read().splitlines()
# Video scaling factor
scale = 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", action="store_true", default=False, help="save background images")
    ap.add_argument("-v", "--video", action="store_true", default=False, help="save bg/fg videos")
    ap.add_argument("-p", "--play", action="store_true", default=False, help="Show current frames (will incur runtime increase)")

    ap.add_argument("-ld", "--lane_detect", action="store_true", default=False, help="lane detection")

    ap.add_argument("-bgr", "--bgratio", action="store", type=float, default=0.9, help="If a foreground pixel keeps semi-constant value for about backgroundRatio*history frames, it's considered background")
    ap.add_argument("-ct", "--complexity", action="store", type=float, default=-1, help="(frames) measure of the maximum portion of the data that can belong to foreground objects without influencing the background model")
    ap.add_argument("-hist", "--history", action="store", type=int, default=128, help="number of last frames that affect the background model.")
    ap.add_argument("-var", "--variance", action="store", type=int, default=9, help="variance threshold for the pixel-model match")
    ap.add_argument("-vinit", "--variance_init", action="store", type=int, default=15, help="initial variance of each gaussian component.")
    ap.add_argument("-nmix", "--nmixtures", action="store", type=int, default=5, help="number of gaussian components in the background model.")
    ap.add_argument("-lr", "--learn_rate", action="store", type=float, default=-1, help="value between 0 and 1 that indicates how fast the background model is learnt")

    arg_in = ap.parse_args()

    bg_subtract(arg_in)



def bg_subtract(arg_in):
    """
    MOG2 Paper: http://www.zoranz.net/Publications/zivkovicPRL2006.pdf
    python3 bgfg_generate.py -v -i -hist 256 -nmix 4 -var 25 -bgr 0.6 -lr 0.005 -ct 256

    """
    global vpath
    vpath = ['../../aic19-track3-test-data/1.mp4']
    # Only run specific videos (specify here)
    # vpath = [vpath[44], vpath[54], vpath[55]]
    for v in vpath:  # Test Videos only, modify this to include other videos
        # Setup VideoCapture object (read Video)
        # cap = cv2.VideoCapture(v + "vdo.avi")
        cap = cv2.VideoCapture(v)

        # Target directory name
        dirname = "./tmp"
        # dirname = "./tmp/{0}_{1}_{2}/".format(*v.split('/')[1:-1])
        mkdir_ifndef(dirname)   # Make directory if not exist

        # get video width/height, modified by scale
        vh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)*scale)
        vw = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*scale)
        if arg_in.video:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            v_out = cv2.VideoWriter(dirname + 'v_out.avi', fourcc, 10.0, (2*vh, 2*vw))
            fg_out = cv2.VideoWriter(dirname + 'fg_roi.avi', fourcc, 10.0, (vh, vw))

        vroi = 255 * np.ones((vw, vh), dtype=np.uint8)
        vroi2 = 255 * np.ones((vw, vh), dtype=np.uint8)
        # Read in ROI images, first is applied before background subtraction
        # vroi = cv2.imread(v + "roi.jpg", cv2.IMREAD_GRAYSCALE)
        # vroi = cv2.resize(vroi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        # Applied after filter
        # vroi2 = cv2.imread(v + "roi.jpg", cv2.IMREAD_GRAYSCALE)
        # vroi2 = cv2.resize(vroi2, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        """MOG2 Background Subtractor
        Background Ratio (TB)               If a foreground pixel keeps semi-constant value for about backgroundRatio*history frames, it's considered background
        Complexity Reduction Threshold (Cf) measure of the maximum portion of the data that can belong to foreground objects without influencing the background model
                                            For a foreground pixel to become background, it should be static for log(1-Cf)/log(1-alpha)

        History:                            number of last frames that affect the background model.
        N-Mixtures:                         number of gaussian components in the background model.
        Variance Threshold (C_thr):         variance threshold for the pixel-model match.
        Initial Variance                    initial variance of each gaussian component.
        """
        bs = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

        bs.setBackgroundRatio(arg_in.bgratio)                   # Background Ratio (def: 0.9)
        bs.setHistory(arg_in.history)                           # History (def 500)
        bs.setNMixtures(arg_in.nmixtures)                       # Number of Gaussian Mixtures (def 5)
        bs.setVarInit(arg_in.variance_init)                     # Initial Variance of new Mixtures (def 15)
        bs.setVarThreshold(arg_in.variance)                     # Variance threshold to trigger (def 16)
        # bs.setComplexityReductionThreshold(arg_in.complexity)   # Complexity Reduction Threshold (def 0.05)
        learn_rate = 0.07                                       # Initial Learning rate

        # conditions for complexity/learning_rate defaults (-1)
        if arg_in.complexity < 0 or arg_in.learn_rate < 0:
            cmpx_reduction_factor = 0.05
            cmpx_reduction_frames = -1
        else:
            cmpx_reduction_frames = arg_in.complexity
            cmpx_reduction_factor = 1 - np.exp(arg_in.complexity * np.log(1-arg_in.learn_rate))

        print("Setting up MOG2 Background subtractor...\n"
              "\tImage Resolution = {:0.0f}x{:0.0f}\n"
              "\tBackground Ratio = {:0.3f}\n"
              "\tHistory = {:0.0f}\n"
              "\tVariance = {:0.0f}\n"
              "\tLearning Rate (< History) = {:0.3f}\n"
              "\tLearning Rate (>= History) = {:0.3f}\n"
              "\tComplexity Reduction Threshold (ratio) = {:0.3f}\n"
              "\tComplexity Reduction Threshold (frames) = {:0.0f}\n"
              "\tN-Mixtures = {:0.0f}".format(vh, vw, bs.getBackgroundRatio(), bs.getHistory(), bs.getVarThreshold(), learn_rate, arg_in.learn_rate, cmpx_reduction_factor, cmpx_reduction_frames,  bs.getNMixtures()))

        # Read every frame of video
        while True:
            ret, frame = cap.read()
            frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)  # Current frame number
            if not ret:  # false if at end of Video
                break

            if frame_num == bs.getHistory():
                learn_rate = arg_in.learn_rate
                bs.setComplexityReductionThreshold(cmpx_reduction_factor)

            # frame = cv2.GaussianBlur(frame, (15, 15), 0)  # Initial Blurring before downscale
            # frame = cv2.blur(frame, (5, 5))  # Initial Blurring before downscale

            frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            frame = cv2.bitwise_and(frame, frame, mask=vroi)  # Initial mask

            fg_img = bs.apply(frame, learningRate=learn_rate)
            bg_img = bs.getBackgroundImage()

            # Remove Shadows
            ret, fg_img = cv2.threshold(fg_img, 192, 255, cv2.THRESH_BINARY)


            # Noise removal functions
            fg_mask = apply_filter(fg_img)
            fg_mask2 = fg_mask.copy()
            fg_mask = cv2.bitwise_and(fg_mask, fg_mask, mask=vroi2)  # Second ROI mask
            # fg_mask = apply_morphology(fg_mask)
            # fg_mask = fill_regions(fg_mask)

            # Segment the foreground using the foreground mask
            fg_seg = cv2.bitwise_and(frame, frame, mask=fg_mask)

            ###############################
            ### Post-processing Done
            ###############################
            # visualization of generating mask
            if arg_in.play:
                # Concatenate frame, background, foreground, segmented foreground
                f1 = np.concatenate((frame, bg_img), axis=0)
                f2 = np.concatenate((cv2.cvtColor(fg_img, cv2.COLOR_GRAY2BGR), fg_seg), axis=0)
                comb_frame = np.concatenate((f1, f2), axis=1)

                cv2.imshow("frame", comb_frame)

                # cv2.imshow("fg", fg_mask2)
                cv2.imshow("fg",  cv2.threshold(cv2.blur(fg_img, (5, 5)), 128, 255, cv2.THRESH_BINARY)[1])

                kp = cv2.waitKey(5)
                if kp == ord('s'):
                    sv_frame = cv2.resize(bg_img, None, fx=1/scale, fy=1/scale)
                    cv2.imwrite(dirname + "bg_img_{0}_{1}_{2}_{3}.jpg".format(*v.split('/')[1:-1], str(uuid.uuid4())[0:10] ), bg_img)
                elif kp == ord('n'):
                    break
                elif kp == ord('q'):
                    cv2.destroyAllWindows()
                    exit(0)
            # Write to output video
            if arg_in.video:
                f1 = np.concatenate((frame, bg_img), axis=0)
                f2 = np.concatenate((cv2.cvtColor(fg_img, cv2.COLOR_GRAY2BGR), fg_seg), axis=0)
                comb_frame = np.concatenate((f1, f2), axis=1)
                fg_out.write(cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2RGB))

                v_out.write(comb_frame)

        # Release VideoCapture instances
        if arg_in.video:
            cap.release()
            v_out.release()
            fg_out.release()
            # bg_out.release()

        # Save background image
        if arg_in.image:
            bg_img = bs.getBackgroundImage()
            cv2.imwrite(dirname + " bg_img_{0}_{1}_{2}.jpg".format(*v.split('/')[1:-1]), bg_img)


def apply_filter(frame):
    """Applies Median and Gaussian filters to remove small spots
    """
    # frame = cv2.blur(frame, (7, 5))
    # ret, frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)
    frame = cv2.medianBlur(frame, 3) # Clear the image, remove small spots
    frame = cv2.GaussianBlur(frame, (3, 3), 0)  # Smooth the image

    # remove noise
    # ret, out = cv2.threshold(out, 192, 255, cv2.THRESH_TOZERO)
    ret, frame = cv2.threshold(frame, 16, 255, cv2.THRESH_BINARY)
    frame = cv2.medianBlur(frame, 3)
    return frame


def apply_morphology(frame):
    """Applies morphological operations to remove noise and to segment vehicles
    """
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 5))
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    # kernel_grad = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel=kernel_open)         # Noise removal
    # frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel=kernel_close)
    frame = cv2.morphologyEx(frame, cv2.MORPH_DILATE, kernel=kernel_dilate)     # Expands detected ROIs
    # frame = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel=kernel_grad)     # Creates ROI outline
    return frame



def fill_regions(frame):
    """Fills in completely bounded regions
    """
    # Threshold.
    # Set values equal to or above 220 to 0.
    # Set values below 220 to 255.
    # th, im_th = cv2.threshold(frame, 220, 255, cv2.THRESH_BINARY_INV);
     
    # Copy the thresholded image.
    im_floodfill = frame.copy()
     
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = frame.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
     
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
     
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
     
    # Combine the two images to get the foreground.
    im_out = frame | im_floodfill_inv
    return im_out


def mkdir_ifndef(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)


if __name__ == "__main__":
    main()

"""
def lane_detect(arg_in):
#     global vpath
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

#     vstart = 0
#     for v in vpath[vstart:]:
#         cap = cv2.VideoCapture(v + "vdo.avi")

#         dirname = "./tmp/{0}_{1}_{2}/".format(*v.split('/')[1:-1])
#         mkdir_ifndef(dirname)

#         vh = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
#         vw = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2)
        
#         frame_hist = arg_in.history
#         varThreshold = arg_in.variance
#         n_mixtures = arg_in.nmixtures
#         learnRate = arg_in.learn_rate

#         bs = cv2.createBackgroundSubtractorMOG2(history=frame_hist, varThreshold=varThreshold, detectShadows=False)
#         # print(bs.getNMixtures())
#         bs.setNMixtures(n_mixtures)
#         bs.setHistory(frame_hist)

#         out = 0
#         while True:
#             ret, frame = cap.read()
#             cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES))
#             if not ret:
#                 break
#             # frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
#             fg_mask = bs.apply(frame, learningRate=learnRate)
#             fg_mask = cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR)

#             bg_img = bs.getBackgroundImage()
#             fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel=kernel)

#             fg = cv2.subtract(frame,bg_img)
#             fg = cv2.cvtColor(fg, cv2.COLOR_BGR2GRAY)

#             out = cv2.bitwise_or(out, fg)
#             out = cv2.medianBlur(out, 3) # Clear the image, remove small spots
#             out = cv2.GaussianBlur(out, (3, 3), 0) # Smooth the image

#             # remove abnormal trajectory
#             ret, out = cv2.threshold(out, 10, 255, cv2.THRESH_TOZERO)
#             ret, out = cv2.threshold(out, 100, 255, cv2.THRESH_BINARY)

#             # visualization of generating mask
#             # cv2.imshow("frame", frame)
#             # cv2.imshow("bg_img", bg_img)
#             # cv2.imshow("fg_img", fg_mask)
#             # cv2.imshow("fg", fg)
#             # cv2.imshow("out", out)
#             # kp = cv2.waitKey(1)

#             # if kp == ord('s'):
#             #     sv_frame = cv2.resize(bg_img, None, fx=2, fy=2)
#             #     cv2.imwrite("bg_img_{0}_{1}_{2}_{3}.jpg".format(*v.split('/')[1:-1], str(uuid.uuid4())[0:10] ), bg_img)
#             # elif kp == ord('q'):
#             #     cv2.destroyAllWindows()
#             #     exit(0)
#         # bg_img = bs.getBackgroundImage()
#         cv2.imwrite("./ld_res/"+"ln_detect_{0}_{1}_{2}.jpg".format(*v.split('/')[1:-1]), out)
#         cap.release()

"""