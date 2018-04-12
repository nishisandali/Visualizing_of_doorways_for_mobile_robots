#In this program I detect the correct threshold points for
# the canny edge detection, which will help me to detect the
# hough's transformation.

##variables##
#s = switch
#canny_edge
#img

##constants##
#k = 27

import cv2

# this function is needed for the createTrackbar step downstream
def nothing(x):
    pass

# read the experimental(Original) image
img = cv2.imread('resize_img4.jpg', 0)

#Edge detection with 0, 0 thresholds
canny_edge = cv2.Canny(img, 0, 0)

# Shows the edge detector picture in a window
cv2.imshow('canny', canny_edge)

# add ON/OFF switch to "canny"
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)

# add lower and upper threshold slidebars to "canny"
cv2.createTrackbar('lower', 'canny', 0, 500, nothing)
cv2.createTrackbar('upper', 'canny', 0, 500, nothing)

# Infinite loop until we hit the escape key on keyboard
while(1):
    #Shows the edge detection change in a window called canny
    cv2.imshow('canny', canny_edge)

    # get current positions of three trackbars
    lower = cv2.getTrackbarPos('lower', 'canny')
    upper = cv2.getTrackbarPos('upper', 'canny')
    s = cv2.getTrackbarPos(switch, 'canny')

    #if switch is 0 show the original image else show the canny edge detection trackbars
    if s == 0:
        canny_edge = img
    else:
        #else Edge detection
        canny_edge = cv2.Canny(img, lower, upper)

    # display images
    cv2.imshow('original', img)
    cv2.imshow('canny', canny_edge)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:   # hit escape to quit
        break
        
cv2.destroyAllWindows()
