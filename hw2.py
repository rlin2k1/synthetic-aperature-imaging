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
from matplotlib import pyplot as plt
import sys

def main():
    cap = cv2.VideoCapture('IMG_0955.MOV')
 
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    # Read until video is completed
    while(cap.isOpened()):
        # # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if ret == True:
            # Display the resulting frame
            cv2.imshow('Frame',frame)
            img = frame
            img2 = img.copy()
            template = cv2.imread('template.png',0)
            w, h = template.shape[::-1]

            # All the 6 methods for comparison in a list
            methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                        'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

            for meth in methods:
                img = img2.copy()
                method = eval(meth)

                # Apply template Matching
                print("REACHED")
                res = cv2.matchTemplate(img,template,method)
                print("REACHED1")
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                print("REACHED1")
                # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                print("REACHED2")
                cv2.rectangle(img,top_left, bottom_right, 255, 2)
                print(res)
                plt.subplot(121)
                print("REACHED5")
                plt.imshow(res,cmap = 'gray')
                print("REACHED4")
                plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                plt.subplot(122),plt.imshow(img,cmap = 'gray')
                plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                plt.suptitle(meth)
                print("REACHED1")
                plt.show()
            cv2.waitKey(0) #Press Enter for Next Object in the Image
            sys.exit()
        else: 
            break

        #----------------------------------------------------------------------------------------------
    
    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()