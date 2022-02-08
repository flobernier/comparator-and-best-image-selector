#!/usr/bin/python
# -*- coding: UTF-8 -*-
from criterion import *

# Constants
CRIT_ID_FILENAME   = 0
CRIT_ID_SIZE       = 1
CRIT_ID_RESOLUTION = 2
CRIT_ID_MEAN_RGB   = 3
CRIT_ID_BRIGHTNESS = 4
CRIT_ID_SATURATION = 5
CRIT_ID_WPP1       = 6
CRIT_ID_WPP2       = 7
CRIT_ID_BLUR       = 8


class CriterionStats:
	def __init__(self, _list):
		self.list = _list	# 2D array containing image info
		self.nb_img = len(self.list)
		self.nb_criteria = len(self.list[0])
		#print ("nb_img ", self.nb_img)
		#print ("nb_crit", self.nb_criteria)
		self.crit_list = [0] * self.nb_criteria

		# Image stats
		self.score_tot = [0] * self.nb_img
		self.score_tot_median = 0
		self.score_tot_std = 0
		self.best_index = -1
		self.high_index = []

		# Criterion objects
		self.criteria = []
		# By default, the file size weight is less important than the others
		# The filename, resolution and mean rgb color criteria are not used
		self.criteria.append(Criterion("name",           0, 0))
		self.criteria.append(Criterion("size (kBytes)", -1, 1)) # Image size (smaller better)
		self.criteria.append(Criterion("resolution",     0, 0))
		self.criteria.append(Criterion("mean RGB color", 0, 0))
		self.criteria.append(Criterion("brightness 2",  +1, 2)) # Brightness (higher better)
		self.criteria.append(Criterion("saturation",    -1, 2)) # Saturation (smaller better)
		self.criteria.append(Criterion("white_pixels1", -1, 2)) # White pixels percentage 1 (smaller better)
		self.criteria.append(Criterion("white_pixels2", -1, 2)) # White pixels percentage 2 (smaller better)
		self.criteria.append(Criterion("blur",          +1, 2)) # Blur (higher better)

		self.getStats()
		self.getTotalScore()


	# @brief 	Get statistics values
	def getStats(self):
		for i in range(self.nb_criteria):
			self.crit_list[i] = self.getRowFrom2DArray(self.list, i)
			#print (self.crit_list[i])
			#if type(self.crit_list[i][0]) is list:
			#	print ("len", len(self.crit_list[i][0]))
			self.criteria[i].computeStats(self.crit_list[i])


	# @brief	Compute total score of the image based on criteria
	def getTotalScore(self):
		# Weighted sum for each image
		for i in range(self.nb_img):
			self.score_tot[i] = 0
			self.score_tot[i] += self.criteria[CRIT_ID_SIZE].score[i]
			self.score_tot[i] += self.criteria[CRIT_ID_BRIGHTNESS].score[i]
			self.score_tot[i] += self.criteria[CRIT_ID_SATURATION].score[i]
			self.score_tot[i] += self.criteria[CRIT_ID_WPP1].score[i]
			self.score_tot[i] += self.criteria[CRIT_ID_WPP2].score[i]
			self.score_tot[i] += self.criteria[CRIT_ID_BLUR].score[i]
		#print ("score_tot:", self.score_tot)

		# Find Best image
		self.best_index = indexesOf(self.score_tot, max(self.score_tot))
		if len(self.best_index) != 1:
			print ("More than one winner", self.best_index)
		else:
			self.best_index = self.best_index[0]

		# Find images with high score
		self.score_tot_median = statistics.median(self.score_tot)
		self.score_tot_std = statistics.stdev(self.score_tot)
		#print ("score_tot median:", self.score_tot_median, "  std:", round(self.score_tot_std, 2))
		for i in range(self.nb_img):
			if self.score_tot[i] >= (self.score_tot_median + self.score_tot_std):
				#print (i, " ", self.score_tot[i])
				self.high_index.append(i)


	def getRowFrom2DArray(self, arr, idx):
		r = []
		for i in range(len(arr)):
			r.append(arr[i][idx])
		return r

