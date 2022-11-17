#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
import time


# @brief	Write list into csv
# @param[in]	list
def writeCSV(list):
	# Filename with current date
	time_str = time.strftime("%Y-%m-%d_%H-%M-%S")
	filename = "log_" + time_str + ".csv"
	#print (filename)

	with open(filename, 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerows(list)

