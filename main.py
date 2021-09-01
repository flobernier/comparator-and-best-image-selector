#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
print ("OpenCV", cv.__version__)
import os
from colors import *
from helper import *

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
[img1_size_s, img2_size_s] = getCmpStrColor(img1_size/1000.0, img2_size/1000.0, -1)
print ("size (kBytes)\t", img1_size_s, "\t\t\t\t", img2_size_s)
print ("resolution \t", img1.shape, "\t\t", img2.shape)

# Mean color
img1_mean = getRGBMean(img1)
img2_mean = getRGBMean(img2)
print ("mean color \t", img1_mean, "\t\t", img2_mean)

# Brightness
img1_b1 = getBrightness1(img1)
img2_b1 = getBrightness1(img2)
[img1_b1_s, img2_b1_s] = getCmpStrColor(img1_b1, img2_b1, +1)
[img1_b1_pcs, img2_b1_pcs] = getCmpStrColor(img1_b1/255*100, img2_b1/255*100, +1, 1)
print ("brightness 1\t", img1_b1_s+",", img1_b1_pcs+"%", "\t\t\t", img2_b1_s+",", img2_b1_pcs+"%")
img1_b2 = getBrightness2(img1)
img2_b2 = getBrightness2(img2)
[img1_b2_s, img2_b2_s] = getCmpStrColor(img1_b2, img2_b2, +1)
[img1_b2_pcs, img2_b2_pcs] = getCmpStrColor(img1_b2/255*100, img2_b2/255*100, +1, 1)
print ("brightness 2\t", img1_b2_s+",", img1_b2_pcs+"%", "\t\t\t", img2_b2_s+",", img2_b2_pcs+"%")
img1_b3 = getBrightness3(img1)
img2_b3 = getBrightness3(img2)
[img1_b3_s, img2_b3_s] = getCmpStrColor(img1_b3, img2_b3, +1)
[img1_b3_pcs, img2_b3_pcs] = getCmpStrColor(img1_b3/255*100, img2_b3/255*100, +1, 1)
print ("brightness 3\t", img1_b3_s+",", img1_b3_pcs+"%", "\t\t\t", img2_b3_s+",", img2_b3_pcs+"%")

# Blur level
img1_blur = getBlurLevel(img1)
img2_blur = getBlurLevel(img2)
[img1_blur_s, img2_blur_s] = getCmpStrColor(img1_blur, img2_blur, +1, 0)
print ("blur \t\t", img1_blur_s, "\t\t\t\t", img2_blur_s)


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


