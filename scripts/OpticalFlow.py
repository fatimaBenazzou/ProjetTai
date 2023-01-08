import numpy as np
import cv2
import argparse
import os
ABSOLUTE_PATH = os.getcwd()

parser = argparse.ArgumentParser(description='Optical flow')
# prend le chemin de la video en tant que 1er argument
parser.add_argument('-i', action='store', dest='input', required=True,
                    help='Input Video.')

arguments = parser.parse_args()

cap = cv2.VideoCapture(ABSOLUTE_PATH+"//"+arguments.input)

ret, frame = cap.read()  # Get one ret and frame
h, w, _ = frame.shape  # Use frame to get width and height
fps = int(cap.get(cv2.CAP_PROP_FPS))
fnb = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # nombre de frames
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # encodage de la video

frameTime = 1  # int(1000 / fps )  # temps d'attente entre frame

writer = cv2.VideoWriter(ABSOLUTE_PATH+"//"+arguments.input[:-4] +
                         "-of.mp4", fourcc, fps, (w, h))  # Video writing device

# Set parameters for ShiTomasi corner detection """SHITOMASI CORNER DETECTION"""
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

# Set parameters for lucas kanade optical flow
lucas_kanade_params = dict(winSize=(15, 15),
                           maxLevel=2,
                           criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
# Used to create our trails for object movement in the images
color = np.random.randint(0, 255, (100, 3))

# Take first frame and find corners in it
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Find inital corner locations
prev_corners = cv2.goodFeaturesToTrack(prev_gray, mask=None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(prev_frame)

frame_counter = 0

while ret:
    frame_counter += 1
    print(round(frame_counter / fnb * 100, 2), flush=True)

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    new_corners, status, errors = cv2.calcOpticalFlowPyrLK(prev_gray,
                                                           frame_gray,
                                                           prev_corners,
                                                           None,
                                                           **lucas_kanade_params)

    # Select and store good points
    good_new = new_corners[status == 1]
    good_old = prev_corners[status == 1]

    # Draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (int(a), int(b)),
                        (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

    img = cv2.add(frame, mask)

    # Show Optical Flow
    # cv2.imshow('Optical Flow - Lucas-Kanade', img)
    writer.write(img)  # Write frame
    # cv2.waitKey(frameTime)

    # Now update the previous frame and previous points
    prev_gray = frame_gray.copy()
    prev_corners = good_new.reshape(-1, 1, 2)

    ret, frame = cap.read()


# cv2.destroyAllWindows()
writer.release()
cap.release()
