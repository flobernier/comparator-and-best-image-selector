#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import os
import math
from colors import *
from criterion_stats import *
from csv_helper import *


# @brief	Get mean RGB values for an image
# @param[in]	img Source image
# @return	Array with RGB values between 0 and 255
def getRGBMean(img):
	channels = cv.mean(img) # BGR channels
	return [round(channels[2]), round(channels[1]), round(channels[0])] # RGB

# @brief	Get mean brightness value for an image
# @param[in]	img Source image
# @return	Mean brightness
def getBrightness1(img):
	# Brightness from Grayscale + mean
	gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	b,g,r,_ = cv.mean(gray_img) # BGR channels
	return b

# @brief	Get mean perceived brightness value for an image
# @param[in]	img Source image
# @return	Mean perceived brightness
def getBrightness2(img):
	# Perceived brightness with RGB
	b,g,r,_ = cv.mean(img) # BRG channels
	return math.sqrt(0.241*r*r + 0.691*g*g + 0.068*b*b)

# @brief	Get mean brightness value for an image
# @param[in]	img Source image
# @return	Mean brightness
def getBrightness3(img):
	# Brightness from HSV
	hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	h,s,v,_ = cv.mean(hsv_img)
	return v

# @brief	Get mean saturation value for an image
# @param[in]	img Source image
# @return	Mean saturation
def getSaturation(img):
	# Saturation from HSV
	hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	h,s,v,_ = cv.mean(hsv_img)
	return s

# @brief	Get white pixels percentage with HSV mask
# @param[in]	img Source image
# @return	White pixels percentage
def getPercentWhite(img):
	# Convert to HSV image
	gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	img = cv.cvtColor(gray_img, cv.COLOR_GRAY2BGR)
	hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	sensitivity = (16, 32)
	percent_white = [None] * len(sensitivity)
	mask = [None] * len(sensitivity)
	for i in range(len(sensitivity)):
		lower_bound = (0, 0, 255 - sensitivity[i])
		upper_bound = (255, sensitivity[i], 255)
		# Create mask
		mask[i] = cv.inRange(hsv_img, lower_bound, upper_bound)
		# Get percentage of white pixels
		height, width = mask[i].shape[:2]
		num_pixels = height * width
		count_white = cv.countNonZero(mask[i])
		percent_white[i] = (count_white/num_pixels)*100.0
	return percent_white

# @brief	Get blur level for an image
# @param[in]	img Source image
# @return	Blur level
def getBlurLevel(img):
	# Blur level is the variance of the Laplacian of the image
	# A higher value mean more focus and less blur
	return cv.Laplacian(img, cv.CV_64F).var()




# @brief	Open image
# @param[in]	img_filename Source image filename
# @return	Image
def openImage(img_filename):
	img = cv.imread(img_filename)
	if img is None:
		print ("Could not read ", img_filename)
	return img


# @brief	Get image information
# @param[in]	img_filename Source image filename
# @param[in]	img_path Source image path + filename
# @param[in]	img Source image
# @return	List of information in the following order
# 		[filename, size, shape, mean_color, brightness, saturation,
#		 white_pixels1, white_pixels2, blur_level]
def getImageInfo(img_path, img_filename, img):
	# Memory size (kBytes)
	img_size = os.path.getsize(img_path)/1000.0
	# Shape (height, width, nb_channels)
	img_shape = (img.shape[1], img.shape[0])
	# Mean RGB color
	img_mean = getRGBMean(img)
	# Brightness
	#img_b1 = getBrightness1(img)
	img_b2 = getBrightness2(img)
	#img_b3 = getBrightness3(img)
	# Saturation
	img_sat = getSaturation(img)
	# White pixel percentage
	img_wpp = getPercentWhite(img)
	img_wpp = [round(i, 1) for i in img_wpp]
	img_wpp1 = img_wpp[0]
	img_wpp2 = img_wpp[1]
	# Blur level
	img_blur = getBlurLevel(img)

	return [img_filename, round(img_size), img_shape, img_mean,
		round(img_b2), round(img_sat), img_wpp1, img_wpp2,
		round(img_blur)]


def getRowFrom2DArray(arr, idx):
	r = []
	for i in range(len(arr)):
		r.append(arr[i][idx])
	return r


# @brief	Print image information to screen
# @param[in]	imgs_info Image information with predefined format
def printImageInfo(imgs_info):
	imgs_nb = len(imgs_info)
	row_names = ["name", "size (kBytes)", "resolution", "mean RGB color",
		     "brightness 2", "saturation", "white_pixels1",
		     "white_pixels2", "blur"]
	max_w_row_names = max(len(i) for i in row_names)
	#print ("max_w_row_names", max_w_row_names, "w_res", 16)

	# Image identifier
	print ("\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print ("img"+str(i+1))
		else : print ("img"+str(i+1), "\t\t", end=" ")
	# Name
	print ("name\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_info[i][0])
		else : print (imgs_info[i][0], "\t", end=" ")
	# Size
	imgs_size = getRowFrom2DArray(imgs_info, 1)
	imgs_size_s = getStrColorList(imgs_size, -1)
	print ("size (kBytes)\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_size_s[i])
		else : print (imgs_size_s[i], "\t\t", end=" ")
	# Resolution
	print ("resolution\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_info[i][2])
		else : print (imgs_info[i][2], "\t", end=" ")
	# Mean RGB color
	print ("mean RGB color\t", end=" ")
	for i in range(imgs_nb):
		rgb = imgs_info[i][3]
		if i == imgs_nb-1:
			print ("["+str(rgb[0])+","+str(rgb[1])+","+str(rgb[2])+"]")
		else :
			print ("["+str(rgb[0])+","+str(rgb[1])+","+str(rgb[2])+"]\t", end=" ")
	# Brightness 2
	imgs_b = getRowFrom2DArray(imgs_info, 4)
	imgs_bpc = [round(imgs_b[i]*100.0/255.0, 1) for i in range(len(imgs_b))]
	imgs_b_s = getStrColorList(imgs_b, +1)
	imgs_bpc_s = getStrColorList(imgs_bpc, +1)
	print ("brightness 2\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_b_s[i]+",", imgs_bpc_s[i]+"%")
		else : print (imgs_b_s[i]+",", imgs_bpc_s[i]+"%", "\t", end=" ")
	# Saturation
	imgs_sat = getRowFrom2DArray(imgs_info, 5)
	imgs_sat_s = getStrColorList(imgs_sat, -1)
	print ("mean saturation\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_sat_s[i])
		else : print (imgs_sat_s[i], "\t\t", end=" ")
	# White pixel percentage 1
	imgs_wpp1 = getRowFrom2DArray(imgs_info, 6)
	imgs_wpp1_s = getStrColorList(imgs_wpp1, -1)
	print ("white pixels1\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_wpp1_s[i]+"%")
		else : print (imgs_wpp1_s[i]+"%", "\t\t", end=" ")
	# White pixel percentage 2
	imgs_wpp2 = getRowFrom2DArray(imgs_info, 7)
	imgs_wpp2_s = getStrColorList(imgs_wpp2, -1)
	print ("white pixels2\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_wpp2_s[i]+"%")
		else : print (imgs_wpp2_s[i]+"%", "\t\t", end=" ")
	# Blur
	imgs_blur = getRowFrom2DArray(imgs_info, 8)
	imgs_blur_s = getStrColorList(imgs_blur, +1)
	print ("blur\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_blur_s[i])
		else : print (imgs_blur_s[i], "\t\t", end=" ")


# @brief	Compute and Print total score for each image
# @param[in]	imgs_info Image information with predefined format
# @return	List of total score for each image
def printImageScore(imgs_info):
	my_stats = CriterionStats(imgs_info)

	imgs_nb = len(imgs_info)
	score_tot_s = getStrColorList(my_stats.score_tot, +1)
	print ("score\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (score_tot_s[i])
		else : print (score_tot_s[i], "\t\t", end=" ")
	print ("Best image is:", my_stats.best_index+1, "<=>", imgs_info[my_stats.best_index][0])

	return my_stats.score_tot


# @brief	Format and Write image information and score to a csv file
# @param[in]	imgs_info Image information with predefined format
# @param[in]	imgs_score List of total score for each image
def saveCSV(imgs_info, imgs_score):
	imgs_nb = len(imgs_info)
	rows_list = []

	# Image identifier
	imgs_id = []
	for i in range(imgs_nb+1):
		if i == 0: imgs_id.append("")
		else: imgs_id.append("img"+str(i))
	rows_list.append(imgs_id)

	# Format rows info
	row_names = ["name", "size (kBytes)", "resolution", "mean RGB color",
		     "brightness 2", "mean saturation", "white pixels1",
		     "white pixels2", "blur"]
	for r in range(len(row_names)):
		row = [row_names[r]] + [str(imgs_info[i][r]) for i in range(imgs_nb)]
		#print (row)
		rows_list.append(row)

	# Score
	rows_list.append(["score"] + [str(imgs_score[i]) for i in range(imgs_nb)])
	#print (rows_list)

	# Write to CSV
	writeCSV(rows_list)

