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
        ret, f = cap.read()
        frame = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

        if ret == True:
            # Display the resulting frame
            cv2.imshow('Frame',frame)
            img = frame
            template = cv2.imread('template.png',0)
            w, h = template.shape[::-1]
            print("{},{}".format(w,h))

            meth = 'cv2.TM_CCOEFF_NORMED'
            method = eval(meth)
            # Apply template Matching
            res = cv2.matchTemplate(img[135:640,270:700],template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = (max_loc[0]+270, max_loc[1]+135)
            bottom_right = (top_left[0] + w, top_left[1] + h)
            
            print(top_left)
            print(bottom_right)
            cv2.rectangle(img,(135,270), (640,700), 255, 2)
            cv2.rectangle(img,top_left, bottom_right, 255, 2)
            #cv2.rectangle(f,(135,270), (640,700), (0,0,255), 2)
            #cv2.rectangle(f,top_left, bottom_right, (255,0,0), 2)
            #cv2.imwrite("annotated_im.jpg", f)
            #sys.exit(1)
            #plt.subplot(121)
            #plt.imshow(f)
            plt.imshow(res,cmap = 'gray')
            plt.xlabel("Pixel location in X Direction")
            plt.ylabel("Pixel location in Y Direction")
            plt.colorbar()
            '''plt.title('Matching Result') #, plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(img,cmap = 'gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)'''
            plt.savefig('cross_cor.png')
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
