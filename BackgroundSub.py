# OpenCV 2.4.13
import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\auros\old_pc\fatima\Miv\TAI\ProjetTai\walking.avi')

# Initlaize background subtractor
foreground_background = cv2.createBackgroundSubtractorMOG2()

frame_counter = 0



while True:
    ret, frame = cap.read()
    frame_counter += 1
    # Apply background subtractor to get our foreground mask
    foreground_mask = foreground_background.apply(frame)
    if frame_counter == int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
        frame_counter = 0  # Or whatever as long as it is the same as next line
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    print(foreground_mask)
    cv2.imshow('Output', foreground_mask)
    if cv2.waitKey(1) == 13:
        break


cap.release()
cv2.destroyAllWindows()