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
    
    # stores the shift locations
    locs_x = []
    locs_y = []

    frames = []
    tl = []
    f0 = []
    cnt = 0
    method = eval('cv2.TM_CCOEFF_NORMED')

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, f = cap.read()

        if ret == True:
            img = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('template_new.png',0)
            w, h = template.shape[::-1]
            print("{},{}".format(w,h))

            # window bounds in the old movie
            # Rockstar
            tlx, tly, brx, bry = 270, 135, 700, 640
            # Mochi
            #tlx, tly, brx, bry = 200, 300, 600, 800
            # window bounds in the new movie
            #tlx, tly, brx, bry = 150, 300, 540, 700

            # if no window is used
            #res = cv2.matchTemplate(img,template,method)
            res = cv2.matchTemplate(img[tlx:brx, tly:bry],template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            top_left = (max_loc[0]+tly, max_loc[1]+tlx)
            # if no window is used
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

            if cnt == 0:
                cv2.imwrite("gray0.png", img)
                try:
                    cv2.rectangle(f,(tly,tlx), (bry,brx), (0,0,255), 2)
                    cv2.rectangle(f,top_left, bottom_right, (255,0,0), 2)
                    cv2.imwrite("annotated_im.jpg", f)
                except:
                    pass
                plt.imshow(res,cmap = 'gray')
                plt.xlabel("Pixel location in X Direction")
                plt.ylabel("Pixel location in Y Direction")
                plt.colorbar()
                plt.savefig('cross_cor.png')
                plt.clf()
            cnt += 1
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
    plt.savefig("shifts.png")
    npavg = np.average(frames, axis=0)
    print(npavg)
    cv2.imwrite("shifted.png", npavg)

if __name__ == "__main__":
    main()
