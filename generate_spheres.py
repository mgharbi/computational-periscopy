import numpy as np 
import cv2
import argparse
import os


def QRcrop(img):

	'''
		ADD IN QR CODE REGISTRATION AND CROPPING
	'''

def unwrap(img, dstheight, dstwidth, interpolationMode):
	print "Unwrapping sphere to equirectangular projection..."
	srcheight = img.shape[0]
	srcwidth = img.shape[1]

	i, j = np.meshgrid(range(dstwidth), range(dstheight))
	i = i.astype(np.float32)
	j = j.astype(np.float32)
	#scales i,j from integer pixel positions (dst) to float values [-1, 1]
	scaledi = (i*2/dstwidth - 1) * np.pi/2
	scaledj = (j*2/dstheight - 1) * np.pi/2

	#x = np.sin(np.pi/2 - scaledj) * np.cos(scaledi)
	y = np.sin(np.pi/2 - scaledj) * np.sin(scaledi)
	z = np.cos(np.pi/2 - scaledj)

	#scales z and y from float values [-1, 1] to float value pixel positions (src)
	map_x = (y + 1)*srcwidth/2
	map_y = (z + 1)*srcheight/2

	unwrapped = cv2.remap(img, map_x, map_y, interpolationMode)
	return unwrapped

def cht(hdr):
	img = cv2.imread(hdr, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
	if img is None:
		print "Image file {} does not exist".format(hdr)
		quit()

	print "Preprocessing image for better edge detection..."
	#guassian blur for better circle detection -- reduces noise to avoid false circle detection
	blur = cv2.GaussianBlur(img, (5,5), 0)
	#convert to grayscale - increase contrast
	gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

	#The CHT algorithm only takes 8-bit images as input, need to convert if the image is in 16bit
	if(gray.dtype == "uint16"):
		gray = (gray/256).astype('uint8')

	#choose a upper threshold value for the CHT's canny edge detection based off of median pixel intensity
	v = np.median(gray)
	sigma = 0.25
	upper = int(min(255, (1.0 + sigma) * v))

	print "Detecting circles..."
	#detect circles in the image
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 300, param1=upper, param2=50, minRadius=10, maxRadius=0)
	#make sure some circles are found
	if circles is not None:
		#convert the (x,y) coordinates and radius of the circles to integers
		circles = np.round(circles[0,:]).astype('int')

		#store cirlce params
		x = circles[0][0]
		y = circles[0][1]
		r = circles[0][2]

		print "Circle found at (%d, %d) with raidus %d" %(x, y, r)
		return circles
	else:
		print "No circles found"
		quit()

def crop(circles, img):
		x = circles[0][0]
		y = circles[0][1]
		r = circles[0][2]

		#create an all black mask the size of the image
		mask = np.zeros(img.shape, dtype=img.dtype)

		if(img.dtype == "uint16"):
			#add a white mask where the circle was detected
			cv2.circle(mask, (x, y), r, (65535, 65535, 65535), -1)
		else:
			#add a white mask where the circle was detected
			cv2.circle(mask, (x, y), r, (255, 255, 255), -1)

		#apply mask 
		masked = cv2.bitwise_and(img, mask)

		#crop image to be centered around the sphere
		cropped = masked[y - r: y + r, x - r: x + r, :]

		return cropped

def generateSpheres(hdr, circles, fnout):
	img = cv2.imread(hdr, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
	if img is None:
		print "Image file {} does not exist".format(hdr)
		quit()
	#isolate the sphere from the rest of the image
	cropped = crop(circles, img)
	#unwrap the image to equirectagular (with a width twice as large)
	unwrapped = unwrap(cropped, cropped.shape[0], 2*cropped.shape[1], cv2.INTER_LINEAR)
	#write the unwrapped image 
	cv2.imwrite(fnout, unwrapped)
	print "Wrote equirectangular image to {}".format(fnout)
	return unwrapped

if __name__ == "__main__":
	#construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required = True, help = "Path to the image")
	args = ap.parse_args()
	fnout = os.path.splitext(filename)[0] + "_sphere" + os.path.splitext(filename)[1]

	print "Generating spheres from {}".format(args.image)
	unwrapped = generateSpheres(args.image, fnout)
	cv2.imshow("unwrapped", unwrapped)
	cv2.waitKey(0)
