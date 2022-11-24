#!/usr/bin/python
# -*- coding: UTF-8 -*-

## PARAMETERS ##
path = "./test/samples3"
FAST_MODE = False

# Similarity parameters
SIMILARITY_WIDTH     = 80   # pixels - Width of the resized image for faster similarity check
SIMILARITY_HEIGHT    = 60   # pixels - Height of the resized image for faster similarity check
MSSISM_MIN_THRESHOLD = 0.3  # % - MSSISM minimum threshold for two similar images

# Criteria parameters
WEIGHT_SIZE          = 0.2  # Image size weight
WEIGHT_BRIGHTNESS    = 2    # Brightness weight
WEIGHT_SATURATION    = 2    # Saturation weight
WEIGHT_WPP1          = 2    # White pixels percentage 1 weight
WEIGHT_WPP2          = 2    # White pixels percentage 2 weight
WEIGHT_BLUR          = 2    # Blur level weight
