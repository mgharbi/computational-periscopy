import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--imagesdir", "-i", help="Directory of images to calculate mean and standard devation"
											  " of intensity to see how the power of the flash degrades over time",
										 required=True)

args = parser.parse_args()

mean_intensities = []
files = []

for file in os.listdir(args.imagesdir):
	if file.endswith("tif"):
		files.append(file)

files.sort()

print files

for file in files:
	img = cv2.imread(os.path.join(args.imagesdir, file), cv2.IMREAD_ANYDEPTH)
	mean = np.mean(img)
	mean_intensities.append(mean)
	print mean
		

overall_mean = np.mean(mean_intensities)
overall_std = np.std(mean_intensities)

print "Overall mean: " + str(overall_mean)
print "Overall std: " + str(overall_std)

times = []

for i in range(1, len(mean_intensities) + 1):
	times.append(i)

fig1 = plt.figure(1)
plt.hist(mean_intensities)
plt.title("Average intensities")
plt.xlabel("intensity")
plt.ylabel("frequency")

fig1.show()

fig2 = plt.figure(2)
plt.plot(times, mean_intensities)
plt.title("Intensity vs Time")
plt.xlabel("Time in s")
plt.ylabel("intensity")

fig2.show()

raw_input()