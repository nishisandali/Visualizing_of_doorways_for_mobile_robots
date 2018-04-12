#In this program, I resize the resolution(size) of the original picture
#Therefore it will help me to test for canny edge detection

##variables##
#img
#img_r

import cv2

#Read the original image
img = cv2.imread('img8.jpg')
#print the resolution of the original image in the console
print(img.shape)
#resize the image to the given resolution sizes
img_r = cv2.resize(img, (240, 320), cv2.INTER_AREA)
#print the new resolution of the image in the console
print(img_r.shape)
#Show the new picture
cv2.imwrite('resize_img8.jpg',img_r)

