#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
print ("OpenCV", cv.__version__)
import os
import time
from colors import *
from helper import *

## PARAMETERS ##
path = "./test/test2"
SHOULD_SHOW = True


## MAIN ##
# Get images paths and filenames in folder
#start = time.perf_counter()
(imgs_path, imgs_filename) = getImgPath(path)
imgs_nb = len(imgs_path)
#end = time.perf_counter()
#print ("time fname", round((end-start)*1000,3), " ms")

# Open images
#start = time.perf_counter()
imgs = []
for path in imgs_path:
	imgs.append(openImage(path))
#end = time.perf_counter()
#print ("time open ", round((end-start)*1000), " ms")

# Get Image info
#start = time.perf_counter()
imgs_info = []
for i in range(imgs_nb):
	imgs_info.append(getImageInfo(imgs_path[i], imgs_filename[i], imgs[i]))
#end = time.perf_counter()
#print ("time gInfo", round((end-start)*1000), " ms")

# Display info
#start = time.perf_counter()
printImageInfo(imgs_info)
imgs_score = printImageScore(imgs_info)
saveCSV(imgs_info, imgs_score)
#end = time.perf_counter()
#print ("time print", round((end-start)*1000,3), " ms")


# Show comparison
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


