import numpy as np 
import cv2
import argparse
import matplotlib.pyplot as plt

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "Path to the image")
ap.add_argument("-s", "--shrink", action="store_true")
args = vars(ap.parse_args())


def autocanny(img, sigma=.33):
	#compute the median of the single channel pixel intensitites
	v = np.median(img)

	#apply automatic Canny edge detection using the computed median
	upper = int(min(255, (1.0 + sigma) * v))
	lower = upper / 2
	edges = cv2.Canny(img, lower, upper)

	print upper

	#return the edged image
	return edges


#Load the image and clone it for output
img = cv2.imread(args['image'], cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
if args["shrink"]:
	img = cv2.resize(img, (0,0), fx=.25, fy=.25)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



#The canney algorithm only takes 8-bit images as input, need to convert if the image is in 16bit
if(gray.dtype == "uint16"):
	gray = (gray/256).astype('uint8')


manual = cv2.Canny(gray, 100, 200)
#adjust low and high hysteresis threshold - to test out what CHT will do (canny computerphile vid)
auto = autocanny(gray)

plt.subplot(121)
plt.imshow(cv2.cvtColor(manual, cv2.COLOR_GRAY2RGB))
plt.subplot(122)
plt.imshow(cv2.cvtColor(auto, cv2.COLOR_GRAY2RGB))
plt.show()
