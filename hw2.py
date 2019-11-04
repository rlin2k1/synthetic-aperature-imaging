""" hw2.py
HOMEWORK 2: SYNTHETIC APERTURE IMAGING

Author(s):
    Jeffrey Lung
    Roy Lin

Date Created:
    November 3rd, 2019
"""
import cv2
import numpy as np
import sys

def main():
    cap = cv2.VideoCapture('IMG_0955.MOV')
 
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("UnNDErthesun.jpg", frame)
        sys.exit(1)
        if ret == True:
            # Display the resulting frame
            cv2.imshow('Frame',frame)
            cv2.waitKey(0) #Press Enter for Next Object in the Image
        else: 
            break
    
    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()