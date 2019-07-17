#!/usr/bin/env python
# coding: utf-8

# # GOTCHA
# **General purpose Online Tool for Captcha HAndling**
# 
# GOTCHA is a python module intended to provide a way for handling [CAPTCHAs](https://en.wikipedia.org/wiki/CAPTCHA) in automated testing. GOTCHA accepts images represented as numpy arrays and returns a character string with its guess. GOTCHA is not meant to be used for bypassing any actual security measures - This is why it will only work with extremely simple captchas such as _Simple PHP CAPTCHA_ or the _Really simple CAPTCHA plugin_ for WordPress. 
# 
# This notebook provides an in-depth explanation of how GOTCHA works and how well it performs.

# ## Dependencies

# GOTCHA requires:
# * Python 3
# * The Python modules listed in the import-section
# * A running installation of tesseract
# 
# Install Tesseract on Debian/Ubuntu:
# ```bash
# $ sudo apt-get install tesseract-ocr
# ```
# 
# Install Tesseract on macOS:
# ```bash
# $ brew install tesseract
# ```
# 

# ## Preparations


# Import relevant libraries
import os
import cv2
import glob
import argparse
import pytesseract
import numpy as np
from PIL import Image
from scipy import ndimage

parser = argparse.ArgumentParser(description="CAPTCHA breaker")
parser.add_argument('img_path', type=str, help="Input file")
parser.add_argument('--deskew',default=True, help="Should the image be deskewed? (default: True)")
parser.add_argument('--pagesegmode', default=11, help="Page segmentation mode for tesseract (default: 11)")
parser.add_argument('--verbose', default=False, help="Show intermediate steps? (default: False)")

args = parser.parse_args()


def solve_captcha(image, deskew=True, pagesegmode=11, verbose=False):
	"""
    Receives a CAPTCHA as input, processes it and returns a string with the guess for the solution.
    
    :praram image:      The CAPTCHA represented as ndarray (via cv2.imread)
    :param deskew:      boolean, whether the image schould be deskewed
    :param pagesegmode: int 0-13, page segmentation mode for tesseract
    :param verbose:     boolean, if True, individual steps are being shown
    :return:            string, the CAPTCHA solution
    """
	if verbose:
		print("Original Image")
		cv2.imshow("Original Image",image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
	if verbose:
		print("Applying Mean Shift Filtering")
		cv2.imshow("Mean shift filtering",shifted)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
    # Skewness corection:
    # https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/

    # Convert to greyscale and perform bitflip to inverse image
	image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image_greyscale = cv2.bitwise_not(image_greyscale)

    # Thresholding the image, setting all foreground pixels to 0 and background pixels to 255.
    # Results in a black and white image
	image_bw = cv2.threshold(image_greyscale, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	if verbose:
		print("Converting to binary image for further processing")
		cv2.imshow("Binary image",image_bw)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

    # Deskew if necessary
	if deskew:
        # Get non-zero pixels
		coords = np.column_stack(np.where(image_bw > 0))
        # Get rotation angle
		angle = cv2.minAreaRect(coords)[-1]
        # Adjust angles to avoid flipping text upside down
		if angle < -45:
			angle = -(90 + angle)
		else:
			angle = -angle
		# Rotation
		(h, w) = image_bw.shape[:2]
		center = (w // 2, h // 2)
		M = cv2.getRotationMatrix2D(center, angle, 1.0)
		image_deskewed = cv2.warpAffine(image_bw, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
		if verbose:
			print("Correcting for skewness")
			cv2.imshow("Deskewed",image_deskewed)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	else:
		image_deskewed = image_bw
    
	# Median Blur
	image_median_blur = cv2.medianBlur(image_deskewed,3)
	if verbose:
		print("Applying median blur")
		cv2.imshow("Median blur",image_median_blur)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# Converting image back to color for kernel methods
	image_median_blur = cv2.cvtColor(image_median_blur,cv2.COLOR_GRAY2BGR)
	# erode and dilate
	kernel = np.ones((2,2),np.uint8)
	image_eroded_dilated= cv2.erode(image_median_blur,kernel,iterations = 1)
	image_eroded_dilated = cv2.dilate(image_eroded_dilated,kernel,iterations = 1)
	# Flip colors
	image_eroded_dilated = (255-image_eroded_dilated)    
	if verbose:
		print("Eroding and delating")
		cv2.imshow("Erosion and delation",image_eroded_dilated)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	# Converting ndarray to image for OCR processing
	ocr_image = Image.fromarray(image_eroded_dilated)
	# Actual ocr
	txt = pytesseract.image_to_string(ocr_image, 
		config="-c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm "+str(pagesegmode))
	return txt

img = cv2.imread(args.img_path)
guess = solve_captcha(img, args.deskew, args.pagesegmode, args.verbose)
print("Guess: "+guess)