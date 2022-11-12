#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np
import math

import os
import time

path = "./test/samples2"
SIMILARITY_WIDTH     = 80 # pixels
SIMILARITY_HEIGHT    = 60 # pixels
MSSISM_MIN_THRESHOLD = 0.3 # % - MSSISM minimum threshold for two similar images


# @brief	Compute Peak Signal to Noise Ratio (PSNR) between two images
# @param[in]	I1 First image
# @param[in]	I2 Second image
# @return	Peak Signal to Noise Ratio
def getPSNR(I1, I2):
	s1 = cv.absdiff(I1, I2) #|I1 - I2|
	s1 = np.float32(s1)     # cannot make a square on 8 bits
	s1 = s1 * s1            # |I1 - I2|^2
	sse = s1.sum()          # sum elements per channel
	if sse <= 1e-10:        # sum channels
		return 0        # for small values return zero
	else:
		shape = I1.shape
		mse = 1.0 * sse / (shape[0] * shape[1] * shape[2])
		psnr = 10.0 * np.log10((255 * 255) / mse)
		return psnr


# @brief	Compute the Mean Structural Similarity (MSSISM) index between two images
# @param[in]	i1 First image
# @param[in]	i2 Second image
# @return	Similarity index between zero and one. One = perfect fit
# @source	https://docs.opencv.org/4.5.2/d5/dc4/tutorial_video_input_psnr_ssim.html
def getMSSISM(i1, i2):
	C1 = 6.5025
	C2 = 58.5225

	# INITS
	I1 = np.float32(i1) # cannot calculate on one byte large values
	I2 = np.float32(i2)
	I2_2 = I2 * I2 # I2^2
	I1_2 = I1 * I1 # I1^2
	I1_I2 = I1 * I2 # I1 * I2

	# PRELIMINARY COMPUTING
	mu1 = cv.GaussianBlur(I1, (11, 11), 1.5)
	mu2 = cv.GaussianBlur(I2, (11, 11), 1.5)

	mu1_2 = mu1 * mu1
	mu2_2 = mu2 * mu2
	mu1_mu2 = mu1 * mu2

	sigma1_2 = cv.GaussianBlur(I1_2, (11, 11), 1.5)
	sigma1_2 -= mu1_2
	sigma2_2 = cv.GaussianBlur(I2_2, (11, 11), 1.5)
	sigma2_2 -= mu2_2
	sigma12 = cv.GaussianBlur(I1_I2, (11, 11), 1.5)
	sigma12 -= mu1_mu2

	t1 = 2 * mu1_mu2 + C1
	t2 = 2 * sigma12 + C2
	t3 = t1 * t2 # t3 = ((2*mu1_mu2 + C1).*(2*sigma12 + C2))

	t1 = mu1_2 + mu2_2 + C1
	t2 = sigma1_2 + sigma2_2 + C2
	t1 = t1 * t2  # t1 =((mu1_2 + mu2_2 + C1).*(sigma1_2 + sigma2_2 + C2))

	ssim_map = cv.divide(t3, t1) # ssim_map =  t3./t1;
	mssim = cv.mean(ssim_map)    # mssim = average of ssim map
	return mssim


# @brief        Open image
# @param[in]    img_filename Source image filename
# @return       Image or None if imread failed
def openImage(img_filename):
	img = cv.imread(img_filename)
	if img is None:
		print ("Could not read ", img_filename)
	return img


# @brief        Similarity check
# @param[in]    imgs_filename List of images file names
# @param[in]    imgs List of images
# @param[in]    imgs_width List of images original width before resizing
# @param[in]    imgs_height List of images original height before resizing
# @return       Group of similar images
def similarityCheck(imgs_filename, imgs, imgs_width, imgs_height):
	similar_img_groups = [[]]
	group_counter = 0
	# Save first img in first group
	similar_img_groups[group_counter].append(imgs_filename[0])

	for i in range(1, len(imgs)):
		#start = time.perf_counter()

		idxA = i-1
		idxB = i
		sim_val = [0, 0, 0, 0]
		psnr_val = 0
		is_similar = True

		# Check images width and height
		if (imgs_width[idxA] != imgs_width[idxB] or imgs_height[idxA] != imgs_height[idxB]):
			# Images have different size and are not in the same group
			print ("DIFF Width/Height: ", imgs_filename[idxA], "and", imgs_filename[idxB])
			is_similar = False

		# Get MSSISM and PSNR
		sim_val = getMSSISM(imgs[idxA], imgs[idxB])
		sim_sum = round(sum(sim_val)/3, 2)
		psnr_val = round(getPSNR(imgs[idxA], imgs[idxB]), 2)

		sim_val = [round(i, 2) for i in sim_val]

		# Check similarity with MSSISM
		if (sim_sum <= MSSISM_MIN_THRESHOLD):
			# Images are not similar
			print ("DIFF MSSISM ", imgs_filename[idxA], "and", imgs_filename[idxB])
			is_similar = False

		# Save img filename in group
		if (is_similar == False):
			group_counter += 1
			similar_img_groups.append([])
		similar_img_groups[group_counter].append(imgs_filename[idxB])
		#print ("group_counter", group_counter, "\t", similar_img_groups)

		#end = time.perf_counter()
		print (imgs_filename[idxA], "and", imgs_filename[idxB],
			"  sim_sum:", sim_sum, "  psnr:", psnr_val, "  similarity:", sim_val)
		#print ("time sim", round((end-start)*1000,3), " ms")

	# Display groups
	for i in range(0, len(similar_img_groups)):
		imgs_nb = len(similar_img_groups[i])
		if (imgs_nb > 0):
			print ("GROUP", i, ": ", similar_img_groups[i][0], "to", similar_img_groups[i][(imgs_nb-1)])




## MAIN ##
# Get images filename in folder
imgs_path = []
for (dirpath, dirnames, imgs_filename) in os.walk(path, topdown=True):
        pass
imgs_filename.sort()
#print (imgs_filename)
imgs_nb = len(imgs_filename)
# Image path
for i in range(imgs_nb):
        imgs_path.append(path + "/" + imgs_filename[i])

# Open images
start = time.perf_counter()
imgs = []
for path in imgs_path:
	img_it = openImage(path)
	if (type(img_it) != type(None)):
	        imgs.append(img_it)
end = time.perf_counter()
print ("time open", round((end-start)*1000,3), " ms")

# Get image size and Resize
imgs_width = []
imgs_height = []
r_imgs = []
for img in imgs:
	imgs_width.append(img.shape[1])
	imgs_height.append(img.shape[0])
min_width  = min(imgs_width)
max_width  = max(imgs_width)
min_height = min(imgs_height)
max_height = max(imgs_height)
print ("w  min", min_width, "  max", max_width)
print ("h  min", min_height, "  max", max_height)
# Resize img for performance
start = time.perf_counter()
for img in imgs:
	dim = (SIMILARITY_WIDTH, SIMILARITY_HEIGHT)
	#img = cv.resize(img, dim, cv.INTER_AREA)
	r_imgs.append(cv.resize(img, dim, cv.INTER_AREA))
end = time.perf_counter()
print ("time resize", round((end-start)*1000,3), " ms")


# Similarity check
#start = time.perf_counter()
similarityCheck(imgs_filename, r_imgs, imgs_width, imgs_height)
#end = time.perf_counter()
#print ("time sim", round((end-start)*1000,3), " ms")
