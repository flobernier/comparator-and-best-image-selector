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


def getCmpColor(val1, val2):
	color_end = ENDC
	if val1 > val2:
		color1 = RED
		color2 = GREEN
	elif val2 > val1:
		color1 = GREEN
		color2 = RED
	else:
		color1 = None
		color_end = None
		color2 = None
	return color1, color2, color_end

def getCmpStrColor(val1, val2, green=-1, round_dec=0):
	color_end = ENDC
	if (val1 > val2 and green == -1) or (val1 < val2 and green == +1):
		color1 = RED
		color2 = GREEN
	elif (val1 > val2 and green == +1) or (val1 < val2 and green == -1):
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
