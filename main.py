#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np
import math
from parameters import *
from src.image import *
from src.helper import *
from src.similarity import *
import os
import time

SHOULD_SHOW = False


## MAIN ##
# Get images paths and filenames in folder
#start = time.perf_counter()
imgs_obj = getImgPath(path)
imgs_nb = len(imgs_obj)
#end = time.perf_counter()
#print ("time fname", round((end-start)*1000,3), " ms")
print ("Number of images: ", imgs_nb)

# Open images
start = time.perf_counter()
for i in range(0, imgs_nb):
	imgs_obj[i].openImage()
end = time.perf_counter()
print ("time open  ", round((end-start)*1000, 0), " ms")

# Get image size and Resize
for i in range(0, imgs_nb):
	imgs_obj[i].updateShape()
# Resize img for performance
#start = time.perf_counter()
for i in range(0, imgs_nb):
	dim = (SIMILARITY_WIDTH, SIMILARITY_HEIGHT)
	imgs_obj[i].resize(dim)
#end = time.perf_counter()
#print ("time resize", round((end-start)*1000, 3), " ms")


# Similarity check
start = time.perf_counter()
groups = [[]]
groups = similarityCheck(imgs_obj)
groups_nb = len(groups)
end = time.perf_counter()
print ("time sim   ", round((end-start)*1000, 3), " ms")
# Display groups
#for i in range(0, len(groups)):
#	group_img_nb = len(groups[i])
#	if (group_img_nb > 0):
#		print ("GROUP", i, ": ", groups[i][0], "to", groups[i][(group_img_nb-1)])


# Get Image info
start = time.perf_counter()
groups_info = [[] for i in range(groups_nb)]
for i in range(0, imgs_nb):
	# Resize image for Fast mode
	if (FAST_MODE == True):
		dim = (int(imgs_obj[i].width/2), int(imgs_obj[i].height/2))
		imgs_obj[i].resize(dim)

	imgs_obj[i].computeImageInfo(FAST_MODE)
	#print ("i:", i, imgs_obj[i].filename, "  group_index:", imgs_obj[i].group_index)
	groups_info[imgs_obj[i].group_index].append(imgs_obj[i].getImageInfo())
	#print (groups_info[imgs_obj[i].group_index])
end = time.perf_counter()
print ("time gInfo ", round((end-start)*1000, 0), " ms")


# Display info
#start = time.perf_counter()
for i in range(0, len(groups_info)):
	group_img_nb = len(groups[i])
	# Do nothing if there is only one image in a group
	if (group_img_nb <= 1):
		continue
	print ("GROUP", i, ": ", groups[i][0], "to", groups[i][(group_img_nb-1)])
#	printImageInfo(groups_info[i])

	# Get images score
	[best_index, high_indexes, imgs_score] = getBestImages(groups_info[i])
	if (type(best_index) == list):
		best_fnames = [groups_info[i][j][0] for j in best_index]
		print ("Best image are:", best_fnames, "")
	else:
		best_fnames = groups_info[i][best_index][0]
		print ("Best image is:", best_fnames)

	if (len(high_indexes) > 1):
		high_fnames = [groups_info[i][j][0] for j in high_indexes]
		print ("High score images:", high_fnames)
	else:
		high_fnames = []
	print ("")
	saveCSV(groups_info[i], imgs_score, best_fnames, high_fnames)
#end = time.perf_counter()
#print ("time print ", round((end-start)*1000, 3), " ms")


'''
# Show comparison
if SHOULD_SHOW:
	# Get list of images for each group of similar images
	disp_imgs = []
	i = 0
	for j in range(0, len(groups[i])):
		for k in range(0, len(imgs_obj)):
			if (imgs_obj[k].filename == groups[i][j]):
				disp_imgs.append(imgs_obj[k].img)
	print (groups[i])
	showComparison(disp_imgs)
'''
