#This program demonstrates line finding with the Hough transform

import math
import cv2
import sys
import numpy as np
import canny_edge

def nothing(x):
    pass

if __name__ == "__main__":
    ## [load]
    filename = "K:/VRES/data/IMG_3211.jpg"

    ##Loads an image
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img_r = cv2.resize(src, (240, 320), cv2.INTER_AREA)

    dst = cv2.Canny(img_r, 0, 0)

    cv2.imshow('canny', dst)

    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'canny', 0, 1, nothing)
    cv2.createTrackbar('lower', 'canny', 0, 500, nothing)
    cv2.createTrackbar('upper', 'canny', 0, 500, nothing)
    switch1 = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch1, 'canny', 0, 1, nothing)

    while (1):
        cv2.imshow('canny', dst)
        lower = cv2.getTrackbarPos('lower', 'canny')
        upper = cv2.getTrackbarPos('upper', 'canny')
        s = cv2.getTrackbarPos(switch, 'canny')
        s1 = cv2.getTrackbarPos(switch1, 'canny')

        if s == 0:
            dst = img_r
        else:
            dst = cv2.Canny(img_r, lower, upper)

        cv2.imshow('original', img_r)
        cv2.imshow('canny', canny_edge)
    ## [edge_detection]
        if s1 == 0:
            dst = cv2.Canny(img_r, lower, upper)
        else:
        # Copy edges to the images that will display the results in BGR
            cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
            cdstP = np.copy(cdst)

        ## [hough_lines]
        #  Standard Hough Line Transform
            lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
        ## [hough_lines]
        ## [draw_lines]
        # Draw the lines
            if lines is not None:
                for i in range(0, len(lines)):
                    rho = lines[i][0][0]
                    theta = lines[i][0][1]
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

                    cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
        ## [draw_lines]

        ## [hough_lines_p]
        # Probabilistic Line Transform
            linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
        ## [hough_lines_p]
        ## [draw_lines_p]
        # Draw the lines
            if linesP is not None:
                for i in range(0, len(linesP)):
                    l = linesP[i][0]
                    cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
        ## [draw_lines_p]
        ## [imshow]
        # Show results
            cv2.imshow("Source", img_r)
            cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
            cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
        ## [imshow]
        ## [exit]
        # Wait and Exit
        #cv2.waitKey()
        ## [exit]
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

