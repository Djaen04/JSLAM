#! /home/johk/anaconda3/envs/slam/bin/python
import cv2
import numpy as np
from matplotlib import pyplot as plt

class Extractor:
    def __init__(self):
        pass

    def getFrame(self, frame):
        # FLANN based Matcher

        frame1 = frame
        frame2 = frame

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # Find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(frame1, None)
        kp2, des2 = sift.detectAndCompute(frame2, None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]

        # Ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i] = [1,0]

        draw_params = dict(matchColor = (0, 255, 0),
                           singlePointColor = (255, 0, 0),
                           matchesMask = matchesMask,
                           flags = 0)

        img3 = cv2.drawMatchesKnn(frame1, kp1, frame2, kp2, matches, None, **draw_params)
        return img3


if __name__ == "__main__":
    cap = cv2.VideoCapture("videos/fastcar.mp4")

    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
    extractor = Extractor()

    while 1:
        # Capture frame by frame and scale it down
        ret, frame = cap.read()
        frame = cv2.resize(frame, (W, H), interpolation=cv2.INTER_LINEAR)

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        match_points = extractor.getFrame(frame)
        plt.imshow(match_points,),plt.show()
        break

        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



