#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import statistics


class Criterion:
	def __init__(self, _name, _order, _weight):
		self.name = _name

		self.min = 0
		self.max = 0
		self.idx_min = 0
		self.idx_max = 0
		self.delta = 0
		self.mean = 0
		self.median = 0
		self.std = 0
		self.order = _order # +1 = Higher is better, -1 = smaller is better
		self.weight = _weight
		self.final_weight = _weight
		self.score = 0 # Weighted score


	# @brief	Compute statistics values, tune weight and compute score for each image
	# @param[in]	list List of criterion values for all images
	def computeStats(self, list):
		nb_img = len(list)
		self.min = min(list)
		self.max = max(list)
		self.idx_min = indexesOf(list, self.min)
		# print ("min:", self.min, "\t idx_min:", self.idx_min)
		self.idx_max = indexesOf(list, self.max)
		# print ("max:", self.max, "\t idx_max:", self.idx_max)

		# Compute stats only for used criterion
		if self.weight != 0:
			self.delta = self.max - self.min
			self.mean = statistics.mean(list)
			self.median = statistics.median(list)
			self.std = statistics.stdev(list)
			#print (self.name, "  min:", self.min, "  max:", self.max,
			#	"  delta:", self.delta, "  mean:", round(self.mean,2),
			#	"  median:", round(self.median,2), "  std:", round(self.std,2))

			# Tune weight
			if self.std == 0:
				# Std = 0 means Delta = 0, all the values are the same
				self.final_weight = 0
			elif self.delta < (0.1*self.median):
				# TODO Should we use delta or std here
				#print ("crit", self.name, " delta < 0.1*median")
				self.final_weight = self.weight / 2.0
			else:
				self.final_weight = self.weight

			self.score = [self.getScore(list, nb_img)[i] * self.final_weight for i in range(nb_img)]
			#print ("")


	# @brief	Compute score of one criterion for each image
	# @param[in]	crit_list Criterion list of values with image order
	# @param[in]	nb_img Number of images in criterion list
	# @return	Score list with image order
	def getScore(self, crit_list, nb_img):
		score = [0] * nb_img
		sorted_list = sorted(crit_list)

		# Lowest score is 0, highest score is (nb_img-1)
		if self.order == +1:
			# Higher is better
			for i in range(nb_img):
				for j in range(nb_img):
					if crit_list[i] == sorted_list[j]:
						score[i] = j
		elif self.order == -1:
			# Smaller is better
			for i in range(nb_img):
				for j in range(nb_img):
					if crit_list[i] == sorted_list[j]:
						score[i] = (nb_img-1) - j
		else:
			print ("Unknown order")

		#print ("score:", score)
		return score



## CONVENIENT FUNCTIONS ##

# @brief	Return the list of indexes with a specific value
# param[in]	list List of numbers
# param[in]	value Value to find in the list
# return	Indexes list of positions of the value in the input list
def indexesOf(list, value):
	indexes = []
	for i in range(len(list)):
		if list[i] == value:
			indexes.append(i)
	return indexes
