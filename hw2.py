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

def warpImg(img, xshift, yshift):
    return 


def main():
    cap = cv2.VideoCapture('IMG_0961.MOV')
 
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    # stores the shift locations
    locs_x = []
    locs_y = []

    frames = []
    tl = []
    f0 = []
    # Read until video is completed
    while(cap.isOpened()):
        # # Capture frame-by-frame
        ret, f = cap.read()

        if ret == True:
            frame = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            #cv2.imshow('Frame',frame)
            img = frame
            template = cv2.imread('template5.png',0)
            w, h = template.shape[::-1]
            print("{},{}".format(w,h))

            meth = 'cv2.TM_CCOEFF_NORMED'
            method = eval(meth)
            # Apply template Matching
            # window bounds in the old movie
            #img[270:700,135:640]
            # window bounds in the new movie
            tlx, tly, brx, bry = 150, 300, 540, 700
            print(img.shape)
            print(template.shape)
            res = cv2.matchTemplate(img[tlx:brx, tly:bry],template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = (max_loc[0]+tlx, max_loc[1]+tly)
            #top_left = (max_loc[0], max_loc[1])
            if len(tl) == 0:
                tl += [top_left[0], top_left[1]]
                f0 = f
            bottom_right = (top_left[0] + w, top_left[1] + h)
            xshift, yshift = -(top_left[0] - tl[0]), -(top_left[1] - tl[1])
            M = np.float32([[1, 0, xshift], [0, 1, yshift]])
            print(M)
            frames.append(cv2.warpAffine(f, M, f.shape[::-1][1:]))
            locs_x.append(top_left[0])
            locs_y.append(top_left[1])
            print(top_left)
            print(bottom_right)
            #cv2.rectangle(img,(135,270), (640,700), 255, 2)
            '''
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
            plt.colorbar()'''
            '''plt.title('Matching Result') #, plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(img,cmap = 'gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)'''
            #plt.savefig('cross_cor.png')
            '''
            plt.show()
            #cv2.waitKey(0) #Press Enter for Next Object in the Image
            sys.exit()
            '''
        else: 
            break

        #----------------------------------------------------------------------------------------------
    
    # When everything done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()
    plt.plot(locs_x, locs_y)
    plt.ylabel("Y Pixel Shift")
    plt.xlabel("X Pixel Shift")
    #plt.show()
    #plt.savefig("shifts.png")
    npavg = np.average(frames, axis=0)
    print(npavg)
    # So it appears good in the displayed image
    cv2.imshow("Shifted", np.sum(frames, axis=0) * 3)
    # What's actually written should involve the average of the pixels
    cv2.imwrite("shifted.png", npavg)
    print(f0)
    print(npavg.shape)
    print(f0.shape)
    cv2.imshow("Og", f0)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
