
"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2
import sys
import numpy as np

def filter_region(image, vertices):
    """
    Create the mask using the vertices and apply it to the input image
    """
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension
    return cv2.bitwise_and(image, mask)

def select_region(image):
    """
    It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    """
    # first, define the polygon by vertices
    rows, cols = image.shape[:2]
    bottom_left  = [cols*0.13, rows*0.95]
    top_left     = [cols*0.13, rows*0.1]
    bottom_right = [cols*0.65, rows*0.95]
    top_right    = [cols*0.65, rows*0.1]
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return filter_region(image, vertices)


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resize_img = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resize_img


if __name__ == "__main__":
    ## [load]
    default_file = "K:/VRES/data/resizeimg.jpg"
    filename = default_file

    ##Loads an image
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img_r = image_resize(src, 240, 320, cv2.INTER_AREA)

    # Check if image is loaded fine
    if img_r is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
    ## [load]

    tr1 = eval(input("What is the threshold 1?"))
    tr2 = eval(input("What is the Threshold 2?"))

    dstc = cv2.Canny(img_r, tr1, tr2, None, 3)
    ## [edge_detection]

    dst = select_region(dstc)
    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    cv2.imwrite('resizeimg_select_region.jpg', cdst)

    ## [hough_lines]
    #  Standard Hough Line Transform
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    ## [hough_lines]
    ## [draw_lines]
    # Draw the lines
    difpa = []
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
            difp = pt2[1] - pt1[1]
            if difp > 0:
                difpa.append(difp)
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
    ## [draw_lines]
    if difpa[0] == difpa[1]:
        print ("Gives two parallel and equal straight lines")
    else:
        print("Doesn't give two equal straight lines")
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
    cv2.waitKey()
    ## [exit]

