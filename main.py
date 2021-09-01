#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import os
print ("OpenCV", cv.__version__)

## PARAMETERS ##
img1_filename = "IMG_A.JPG"
img2_filename = "IMG_B.JPG"
SHOULD_SHOW = True


## MAIN ##
# Open images
img1 = cv.imread(img1_filename)
img2 = cv.imread(img2_filename)

if img1 is None:
	print ("Could not read ", img1_filename)
if img2 is None:
	print ("Could not read ", img2_filename)

# Display info
print ("\t\t img1 \t\t\t\t img2")
print ("name \t\t", img1_filename, "\t\t\t", img2_filename)
img1_size = os.path.getsize(img1_filename)
img2_size = os.path.getsize(img2_filename)
print ("size (kBytes)\t", round(img1_size/1000), "\t\t\t\t", round(img2_size/1000))
print ("resolution \t", img1.shape, "\t\t", img2.shape)


if SHOULD_SHOW:
	# Resize
	w = 360.0
	r = w / img1.shape[1]
	dim = (int(w), int(img1.shape[0] * r))
	img1 = cv.resize(img1, dim, cv.INTER_AREA)
	img2 = cv.resize(img2, dim, cv.INTER_AREA)

	# Concatenate
	img0 = cv.hconcat([img1, img2])

	cv.imshow("Comparison", img0)
	cv.waitKey(0)


