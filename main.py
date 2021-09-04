#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
print ("OpenCV", cv.__version__)
import os
import time
from colors import *
from helper import *

## PARAMETERS ##
img1_filename = "IMG_A.JPG"
img2_filename = "IMG_B.JPG"
img3_filename = "IMG_C.JPG"
img4_filename = "IMG_D.JPG"
imgs_filename = [img1_filename, img2_filename, img3_filename, img4_filename]
imgs_nb = len(imgs_filename)
SHOULD_SHOW = True


## MAIN ##
imgs = []
imgs_info = []
# Open images
for filename in imgs_filename:
	imgs.append(openImage(filename))

# Display info
for i in range(imgs_nb):
	imgs_info.append(getImageInfo(imgs_filename[i], imgs[i]))

printImageInfo(imgs_info)

"""
print ("\n")
print ("\t\t img1 \t\t\t\t img2")
print ("name \t\t", img1_filename, "\t\t\t", img2_filename)
[img1_size_s, img2_size_s] = getCmpStrColor(img1_info[1], img2_info[1], -1)
print ("size (kBytes)\t", img1_size_s, "\t\t\t\t", img2_size_s)
print ("resolution \t", img1_info[2], "\t\t", img2_info[2])
print ("mean RGB color \t", img1_info[3], "\t\t", img2_info[3])
[img1_b2_s, img2_b2_s] = getCmpStrColor(img1_info[4], img2_info[4], +1)
[img1_b2_pcs, img2_b2_pcs] = getCmpStrColor(img1_info[4]/255*100, img2_info[4]/255*100, +1, 1)
print ("brightness 2\t", img1_b2_s+",", img1_b2_pcs+"%", "\t\t\t", img2_b2_s+",", img2_b2_pcs+"%")
[img1_blur_s, img2_blur_s] = getCmpStrColor(img1_info[5], img2_info[5], +1, 0)
print ("blur \t\t", img1_blur_s, "\t\t\t\t", img2_blur_s)
[img1_sat_s, img2_sat_s] = getCmpStrColor(img1_info[6], img2_info[6], -1, 0)
print ("saturation \t", img1_sat_s, "\t\t\t\t", img2_sat_s)
"""

if SHOULD_SHOW:
	# Resize
	w = 1280/imgs_nb
	r = w / imgs[0].shape[1]
	dim = (int(w), int(imgs[0].shape[0] * r))
	r_imgs = [cv.resize(i, dim, cv.INTER_AREA) for i in imgs]

	# Concatenate
	img0 = cv.hconcat(r_imgs)

	cv.imshow("Comparison", img0)
	cv.waitKey(0)


