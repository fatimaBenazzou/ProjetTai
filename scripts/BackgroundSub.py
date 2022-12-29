# # OpenCV 2.4.13
import numpy as np
import cv2
import argparse
import os

ABSOLUTE_PATH = os.getcwd()

parser = argparse.ArgumentParser(description='Background subtraction')
# prend le chemin de la video en tant que 1er argument
parser.add_argument('-i', action='store', dest='input', required=True,
                    help='Input Video.')

# prend le nom de la video resultante en tant que 2eme argument
parser.add_argument('-o', action='store', dest='output', required=True,
                    help='Output Video.')
arguments = parser.parse_args()

cap = cv2.VideoCapture(ABSOLUTE_PATH+"//"+arguments.input)
frameCounter = 0

# Initlaize background subtractor
foreground_background = cv2.createBackgroundSubtractorMOG2()

ret, frame = cap.read()  # Get one ret and frame
h, w, _ = frame.shape  # Use frame to get width and height
fps = int(cap.get(cv2.CAP_PROP_FPS))
fnb = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # nombre de frames

# XVID is the ID, can be changed to anything
fourcc = cv2.VideoWriter_fourcc(*"XVID")
frameTime = int(1000 / fps / 10)  # Calculate
writer = cv2.VideoWriter(ABSOLUTE_PATH+"//"+arguments.output +
                         ".avi", fourcc, fps, (w, h))  # Video writing device
writerM = cv2.VideoWriter(ABSOLUTE_PATH+"//"+arguments.output +
                          "-Mask.avi", fourcc, fps, (w, h))  # Video writing device

while ret:  # Use the ret to determin end of video
    print(int(frameCounter / fnb * 100))
    foreground_mask = foreground_background.apply(frame)
    foreground_mask = cv2.cvtColor(foreground_mask, cv2.COLOR_GRAY2RGB)

    newFrame = cv2.bitwise_and(frame, foreground_mask)
    writerM.write(foreground_mask)  # Write frame
    writer.write(newFrame)  # Write frame
    frameCounter += 1

    ret, frame = cap.read()

writerM.release()
writer.release()
cap.release()
