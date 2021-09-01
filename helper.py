#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2 as cv
import math


def getRGBMean(img):
	channels = cv.mean(img) # BGR channels
	return [round(channels[2]), round(channels[1]), round(channels[0])] # RGB


def getBrightness1(img):
	# Get Brightness from Grayscale + mean
	gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	b,g,r,_ = cv.mean(gray_img) # BGR channels
	return b

def getBrightness2(img):
	# Perceived brightness with RGB
	b,g,r,_ = cv.mean(img) # BRG channels
	return math.sqrt(0.241*r*r + 0.691*g*g + 0.068*b*b)

def getBrightness3(img):
	# Get Brightness from HSV
	hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
	h,s,v,_ = cv.mean(hsv_img)
	return v


