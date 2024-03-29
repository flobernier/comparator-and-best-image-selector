#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np
import math
from parameters import *


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


# @brief        Similarity check
# @param[in]    imgs_obj List of images object with filename, width, height and r_img data
# @return       List of groups of similar images
def similarityCheck(imgs_obj):
	similar_img_groups = [[]]
	group_counter = 0
	# Save first img in first group
	similar_img_groups[group_counter].append(imgs_obj[0].filename)
	imgs_obj[0].group_index = group_counter

	for i in range(1, len(imgs_obj)):
		#start = time.perf_counter()
		idxA = i-1
		idxB = i
		sim_val = [0, 0, 0, 0]
		psnr_val = 0
		is_similar = True

		# Check images width and height
		if (imgs_obj[idxA].width != imgs_obj[idxB].width or imgs_obj[idxA].height != imgs_obj[idxB].height):
			# Images have different size and are not in the same group
			#print ("DIFF Width/Height: ", imgs_obj[idxA].filename, "and", imgs_obj[idxB].filename)
			is_similar = False

		# Get MSSISM and PSNR
		sim_val = getMSSISM(imgs_obj[idxA].r_img, imgs_obj[idxB].r_img)
		sim_sum = round(sum(sim_val)/3, 2)
		psnr_val = round(getPSNR(imgs_obj[idxA].r_img, imgs_obj[idxB].r_img), 2)

		sim_val = [round(i, 2) for i in sim_val]

		# Check similarity with MSSISM
		if (sim_sum <= MSSISM_MIN_THRESHOLD):
			# Images are not similar
			#print ("DIFF MSSISM ", imgs_obj[idxA].filename, "and", imgs_obj[idxB].filename)
			is_similar = False

		# Save img filename in group
		if (is_similar == False):
			group_counter += 1
			similar_img_groups.append([])
		similar_img_groups[group_counter].append(imgs_obj[idxB].filename)
		imgs_obj[idxB].group_index = group_counter
		#print ("group_counter", group_counter, "\t", similar_img_groups)

		#end = time.perf_counter()
		#print (imgs_obj[idxA].filename, "and", imgs_obj[idxB].filename,
		#	"  sim_sum:", sim_sum, "  psnr:", psnr_val, "  similarity:", sim_val)
		#print ("time sim", round((end-start)*1000,3), " ms")

	return similar_img_groups

