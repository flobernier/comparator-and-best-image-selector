#!/usr/bin/python
# -*- coding: UTF-8 -*-

# COLORS
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def getCmpStrColor(val1, val2, order=-1, round_dec=0):
	color_end = ENDC
	if (val1 > val2 and order == -1) or (val1 < val2 and order == +1):
		color1 = RED
		color2 = GREEN
	elif (val1 > val2 and order == +1) or (val1 < val2 and order == -1):
		color1 = GREEN
		color2 = RED
	else:
		color1 = None
		color_end = None
		color2 = None

	if round_dec > 0:
		str1 = color1 + str(round(val1, round_dec)) + color_end
		str2 = color2 + str(round(val2, round_dec)) + color_end
	elif round_dec == 0:
		str1 = color1 + str(round(val1)) + color_end
		str2 = color2 + str(round(val2)) + color_end
	else:
		str1 = color1 + str(val1) + color_end
		str2 = color2 + str(val2) + color_end

	return str1, str2


# @brief	Compare list of values and return String list with green and red color for max and min values
# @param[in]	list List of values to compare
# @param[in]	order Color order, +1 => max = green and min = red
# @return	String list with green and red color for max and min values
def getStrColorList(list, order=+1):
	# Find min and max in list
	# TODO check time performance of max and min
	max_idx = list.index(max(list))
	min_idx = list.index(min(list))

	# Convert list to string
	color_str = []
	for i in range(len(list)):
		if (i == max_idx and order == +1) or (i == min_idx and order == -1):
			color_str.append(GREEN + str(list[i]) + ENDC)
		elif (i == min_idx and order == +1) or (i == max_idx and order == -1):
			color_str.append(RED + str(list[i]) + ENDC)
		else:
			color_str.append(str(list[i]))
	return color_str


