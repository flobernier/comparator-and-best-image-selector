#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import os
from src.helper import *


# @brief	Get the list of the images paths and filenames inside the source folder
# @param[in]	path Source folder path
# @return	List of images objects
def getImgPath(path):
	imgs_obj = []
	# Get filenames from path
	imgs_filename = os.listdir(path)
	imgs_filename.sort()
	#print (imgs_filename)

	# Add images path to list only for supported format
	sup_format = [".jpeg", ".jpg", ".png", ".bmp"]
	for filename in imgs_filename:
		ext = os.path.splitext(filename)[1]
		#print (filename, " ", ext)
		if ext.casefold() in (format.casefold() for format in sup_format):
			img_path = path + "/" + filename
			imgs_obj.append(ImageClass(img_path, filename))

	return imgs_obj


# @brief	ImageClass class
class ImageClass:
	def __init__(self, _path, _filename):
		self.path = _path
		self.filename = _filename
		self.group_index = 0
		self.size = 0 # kBytes

		# OpenCV
		self.img = None
		self.r_img = None

		self.height = 0 # pixels
		self.width  = 0 # pixels

		# Mean RGB Color
		self.mean_rgb = 0
		# Brightness
		self.brightness = 0
		# Saturation
		self.saturation = 0
		# White pixel percentage
		self.wpp1 = 0
		self.wpp2 = 0
		# Blur level
		self.blur = 0


	# @brief	Open Image
	def openImage(self):
		self.img = cv.imread(self.path)
		if self.img is None:
			print ("Could not read ", self.filename)

	# @brief	Set internal height and width data
	def updateShape(self):
		self.height = self.img.shape[0]
		self.width  = self.img.shape[1]

	# @brief	Resize image
	# @param[in]	dim Dimension list (width, height) in pixels
	def resize(self, dim):
		self.r_img = cv.resize(self.img, dim, cv.INTER_AREA)

	# @brief	Compute image information
	# @param[in]	use_resize Boolean to choose if image is the resized version or the original image
	def computeImageInfo(self, use_resize=False):
		if (use_resize == True):
			img = self.r_img
		else:
			img = self.img

		# Image shape (width, height)
		self.shape = (img.shape[1], img.shape[0])
		# Memory size (kBytes)
		self.size = os.path.getsize(self.path)/1000.0
		# Mean RGB color
		self.mean_rgb = getRGBMean(img)
		# Brightness
		#self.brightness = getBrightness1(img)
		self.brightness = getBrightness2(img)
		#self.brightness = getBrightness3(img)
		# Saturation
		self.saturation = getSaturation(img)
		# White pixel percentage
		img_wpp = getPercentWhite(img)
		img_wpp = [round(i, 1) for i in img_wpp]
		self.wpp1 = img_wpp[0]
		self.wpp2 = img_wpp[1]
		# Blur level
		self.blur = getBlurLevel(img)

	# @brief	Get image information
	# @return	List of information in the following order
	# 		[filename, size, shape, mean_color, brightness, saturation,
	#		 white_pixels1, white_pixels2, blur_level]
	def getImageInfo(self):
		return [self.filename, round(self.size), self.shape, self.mean_rgb,
			round(self.brightness), round(self.saturation), self.wpp1, self.wpp2,
			round(self.blur)]
