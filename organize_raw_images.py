import os
import sys
import subprocess
import argparse

#Construct and configure argument parser
parser = argparse.ArgumentParser(description="Seperates image dump from SD card into directories defined by capture metadata")
parser.add_argument("--meta", dest="metadatafiles", metavar = "F", nargs='+', help="metadata files listing which images correspond to which captures")
parser.add_argument("--dest", dest="destination", required=True, help="desintation path for new directories")
args = parser.parse_args()


def executeCommand(cmd):
	#execute a terminal command as a subprocess
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #intercept stdout of a subprocess
    for stdout_line in iter(popen.stdout.readline, ""):
    	yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
    	raise subprocess.CalledProcessError(return_code, cmd)

def executeAndPrintCommand(cmd):
	#print subprocess stdout as it happens
	for line in executeCommand(cmd):
		sys.stdout.write(">" + line)
		sys.stdout.flush()

for file in args.metadatafiles:
	if (os.path.isfile(file)):
		print "\nReading metadata file " + os.path.basename(file)	
		f = open(file, "r")
		contents = f.readlines()
		f.close()
	else: 
		print "Metadata file {} does not exist".format(os.path.abspath(file))
		quit()

	#names capture after filename between first underscore and .txt extension
	capturename = file.split("_",1)[1][:-4]
	newdir = os.path.abspath(os.path.join(args.destination, capturename))
	currentdir = os.path.dirname(os.path.abspath(file))
	
	cmd = ["mkdir", "-p", "-v", newdir]
	executeAndPrintCommand(cmd)

	print "Moving .ARW and .JPG files to " + newdir

	for i in range(1, len(contents)):
		ID, phi, theta, raw = contents[i].split()
		rawfile = os.path.join(currentdir, raw)
		if(os.path.isfile(rawfile)):
			cmd = ['mv', rawfile, newdir]
			executeAndPrintCommand(cmd)
		jpgfile = os.path.join(currentdir, raw[:-3]+"JPG")
		if(os.path.isfile(jpgfile)):
			cmd = ['mv', jpgfile, newdir]
			executeAndPrintCommand(cmd)

	print "Moving .txt metadata file to " + newdir

	cmd = ['mv', file, newdir]
	executeAndPrintCommand(cmd)