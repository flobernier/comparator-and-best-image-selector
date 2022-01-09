#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import statistics

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
		self.best_index = -1

		# Criterion stats
		self.crit_min     = [0] * self.nb_criteria
		self.crit_max     = [0] * self.nb_criteria
		self.crit_idx_min = [0] * self.nb_criteria
		self.crit_idx_max = [0] * self.nb_criteria
		self.crit_delta   = [0] * self.nb_criteria
		self.crit_mean    = [0] * self.nb_criteria
		self.crit_median  = [0] * self.nb_criteria
		self.crit_std     = [0] * self.nb_criteria
		# By default, the file size criterion is less important than the others
		# The filename, resolution and mean rgb color criteria are not used
		self.crit_weight  = [0, 1, 0, 0, 2, 2, 2, 2, 2]

		self.computeStats()
		self.getTotalScore()

	# @brief 	Compute statistics values
	def computeStats(self):
		for i in range(self.nb_criteria):
			self.crit_list[i] = self.getRowFrom2DArray(self.list, i)
			#print (self.crit_list[i])
			#if type(self.crit_list[i][0]) is list:
			#	print ("len", len(self.crit_list[i][0]))
			self.crit_min[i] = min(self.crit_list[i])
			self.crit_max[i] = max(self.crit_list[i])
			self.crit_idx_min[i] = self.indexesOf(self.crit_list[i], self.crit_min[i])
			#print ("min:", self.crit_min[i], "\t idx_min:", self.crit_idx_min[i])
			self.crit_idx_max[i] = self.indexesOf(self.crit_list[i], self.crit_max[i])

			# Not for string or list of int
			if i != CRIT_ID_FILENAME and i != CRIT_ID_RESOLUTION and i != CRIT_ID_MEAN_RGB:
				self.crit_delta[i] = self.crit_max[i] - self.crit_min[i]
				self.crit_mean[i] = statistics.mean(self.crit_list[i])
				self.crit_median[i] = statistics.median(self.crit_list[i])
				self.crit_std[i] = statistics.stdev(self.crit_list[i])
				#print ("i:", i, "  min:", self.crit_min[i], "  max:", self.crit_max[i],
				#	"  delta:", self.crit_delta[i], "  mean:", round(self.crit_mean[i],2),
				#	"  median:", round(self.crit_median[i],2), "  std:", round(self.crit_std[i],2))
				if i in [CRIT_ID_SIZE, CRIT_ID_SATURATION, CRIT_ID_WPP1, CRIT_ID_WPP2]:
					self.getCriterionScore(self.crit_list[i], self.nb_img, -1)
				elif i in [CRIT_ID_BRIGHTNESS, CRIT_ID_BLUR]:
					self.getCriterionScore(self.crit_list[i], self.nb_img, +1)
				else:
					print ("error i:", i)
				#print ("")


	# @brief	Compute total score of the image based on criteria
	def getTotalScore(self):
		# Tune weights
		for i in range(self.nb_criteria):
			if self.crit_std[i] == 0:
				# Std = 0 means Delta = 0, all the values are the same
				self.crit_weight[i] = 0
			if self.crit_delta[i] < (0.1*self.crit_median[i]):
				# TODO Should we use delta or std here
				#print ("crit", i, " delta < 0.1*median")
				self.crit_weight[i] = self.crit_weight[i] / 2.0

		# Image size (smaller better)
		size_score = self.getCriterionScore(self.crit_list[CRIT_ID_SIZE], self.nb_img, -1)
		# Brightness (higher better)
		brightness_score = self.getCriterionScore(self.crit_list[CRIT_ID_BRIGHTNESS], self.nb_img, +1)
		# Mean saturation (smaller better)
		sat_score = self.getCriterionScore(self.crit_list[CRIT_ID_SATURATION], self.nb_img, -1)
		# White pixels percentage 1 (smaller better)
		wpp1_score = self.getCriterionScore(self.crit_list[CRIT_ID_WPP1], self.nb_img, -1)
		# White pixels percentage 2 (smaller better)
		wpp2_score = self.getCriterionScore(self.crit_list[CRIT_ID_WPP2], self.nb_img, -1)
		# Blur (higher better)
		blur_score = self.getCriterionScore(self.crit_list[CRIT_ID_BLUR], self.nb_img, +1)

		# Weighted sum for each image
		for i in range(self.nb_img):
			self.score_tot[i] += size_score[i] * self.crit_weight[CRIT_ID_SIZE]
			self.score_tot[i] += brightness_score[i] * self.crit_weight[CRIT_ID_BRIGHTNESS]
			self.score_tot[i] += sat_score[i] * self.crit_weight[CRIT_ID_SATURATION]
			self.score_tot[i] += wpp1_score[i] * self.crit_weight[CRIT_ID_WPP1]
			self.score_tot[i] += wpp2_score[i] * self.crit_weight[CRIT_ID_WPP2]
			self.score_tot[i] += blur_score[i] * self.crit_weight[CRIT_ID_BLUR]
		print ("score_tot:", self.score_tot)

		# Best image
		self.best_index = self.indexesOf(self.score_tot, max(self.score_tot))
		if len(self.best_index) != 1:
			print ("More than one winner", self.best_index)
		else:
			self.best_index = self.best_index[0]


	# @brief	Compute score of one criterion for each image
	# @param[in]	crit_list Criterion list of values with image order
	# @param[in]	nb_img Number of images in criterion list
	# @param[in]	better +1 = Higher is better, -1 = Smaller is better
	# @return	Score list with image order
	def getCriterionScore(self, crit_list, nb_img, better):
		score = [0] * nb_img
		sorted_list = sorted(crit_list)

		# Lowest score is 0, highest score is (nb_img-1)
		if better == +1:
			# Higher is better
			for i in range(nb_img):
				for j in range(nb_img):
					if crit_list[i] == sorted_list[j]:
						score[i] = j
		elif better == -1:
			# Smaller is better
			for i in range(nb_img):
				for j in range(nb_img):
					if crit_list[i] == sorted_list[j]:
						score[i] = (nb_img-1) - j
		else:
			print ("Unknown order")

		#print ("score:", score)
		return score

	# @brief	Return the list of indexes with a specific value
	# param[in]	list List of numbers
	# param[in]	value Value to find in the list
	# return	Indexes list of positions of the value in the input list
	def indexesOf(self, list, value):
		indexes = []
		for i in range(len(list)):
			if list[i] == value:
				indexes.append(i)
		return indexes


	def getRowFrom2DArray(self, arr, idx):
		r = []
		for i in range(len(arr)):
			r.append(arr[i][idx])
		return r

