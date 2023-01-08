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

arguments = parser.parse_args()

cap = cv2.VideoCapture(ABSOLUTE_PATH+"//"+arguments.input)
frameCounter = 0

# Initlaize background subtractor
foreground_background = cv2.createBackgroundSubtractorMOG2()

ret, frame = cap.read()  # Get one ret and frame
h, w, _ = frame.shape  # Use frame to get width and height
fps = int(cap.get(cv2.CAP_PROP_FPS))
fnb = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # nombre de frames
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # encodage de la video

frameTime = 1  # int(1000 / fps )  # temps d'attente entre frame

writer = cv2.VideoWriter(ABSOLUTE_PATH+"//"+arguments.input[:-4] +
                         "-subb.mp4", fourcc, fps, (w, h))  # Video writing device
writerM = cv2.VideoWriter(ABSOLUTE_PATH+"//"+arguments.input[:-4] +
                          "-mask.mp4", fourcc, fps, (w, h))  # Video writing device

while ret:  # Use the ret to determin end of video
    frameCounter += 1
    print(round(frameCounter / fnb * 100, 2), flush=True) 
    foreground_mask = foreground_background.apply(
        frame)  # cree un masque sans le bg
    # reshape la matrice du masque de 1 a 3 channels
    foreground_mask = cv2.cvtColor(foreground_mask, cv2.COLOR_GRAY2RGB)
    # soustraction en utilisant le masque (eyweli rgb : frame*masque)
    newFrame = cv2.bitwise_and(frame, foreground_mask)
    writerM.write(foreground_mask)  # Write frame
    writer.write(newFrame)  # Write frame

    ret, frame = cap.read()

writerM.release()
writer.release()
cap.release()
