#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import math


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
