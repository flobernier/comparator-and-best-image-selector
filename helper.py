#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import os
import math
from colors import *


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
# @param[in]	img Source image
# @return	List of information in the following order
# 		[filename, size, shape, mean_color, brightness, blur_level, saturation]
def getImageInfo(img_filename, img):
	# Memory size (kBytes)
	img_size = os.path.getsize(img_filename)/1000.0
	# Shape (h, w, d)
	img_shape = img.shape
	# Mean RGB color
	img_mean = getRGBMean(img)
	# Brightness
	#img_b1 = getBrightness1(img)
	img_b2 = getBrightness2(img)
	#img_b3 = getBrightness3(img)
	# Saturation
	img_sat = getSaturation(img)
	# Blur level
	img_blur = getBlurLevel(img)

	return [img_filename, round(img_size), img_shape, img_mean,
		round(img_b2), round(img_sat), round(img_blur)]


def getRowFrom2DArray(arr, idx):
	r = []
	for i in range(len(arr)):
		r.append(arr[i][idx])
	return r


def printImageInfo(imgs_info):
	imgs_nb = len(imgs_info)
	row_names = ["name", "size (kBytes)", "resolution",
		"mean RGB color", "brightness 2", "blur", "saturation"]
	max_w_row_names = max(len(i) for i in row_names)
	print ("max_w_row_names", max_w_row_names, "w_res", 16)

	# Image identifier
	print ("\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print ("img"+str(i+1))
		else : print ("img"+str(i+1), "\t\t\t", end=" ")
	# Name
	print ("name\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_info[i][0])
		else : print (imgs_info[i][0], "\t\t", end=" ")
	# Size
	imgs_size = getRowFrom2DArray(imgs_info, 1)
	imgs_size_s = getStrColorList(imgs_size, -1)
	print ("size (kBytes)\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_size_s[i])
		else : print (imgs_size_s[i], "\t\t\t", end=" ")
	# Resolution
	print ("resolution\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_info[i][2])
		else : print (imgs_info[i][2], "\t", end=" ")
	# Mean RGB color
	print ("mean RGB color\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_info[i][3])
		else : print (imgs_info[i][3], "\t", end=" ")
	# Brightness 2
	imgs_b = getRowFrom2DArray(imgs_info, 4)
	imgs_bpc = [round(imgs_b[i]*100.0/255.0, 1) for i in range(len(imgs_b))]
	imgs_b_s = getStrColorList(imgs_b, +1)
	imgs_bpc_s = getStrColorList(imgs_bpc, +1)
	print ("brightness 2\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_b_s[i]+",", imgs_bpc_s[i]+"%")
		else : print (imgs_b_s[i]+",", imgs_bpc_s[i]+"%", "\t\t", end=" ")
	# Saturation
	imgs_sat = getRowFrom2DArray(imgs_info, 5)
	imgs_sat_s = getStrColorList(imgs_sat, -1)
	print ("saturation\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_sat_s[i])
		else : print (imgs_sat_s[i], "\t\t\t", end=" ")
	# Blur
	imgs_blur = getRowFrom2DArray(imgs_info, 6)
	imgs_blur_s = getStrColorList(imgs_blur, +1)
	print ("blur\t\t", end=" ")
	for i in range(imgs_nb):
		if i == imgs_nb-1: print (imgs_blur_s[i])
		else : print (imgs_blur_s[i], "\t\t\t", end=" ")

