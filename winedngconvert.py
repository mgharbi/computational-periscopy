import os
import sys
import subprocess
import argparse

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

'''

How to find windows programs (in C:\ drive)
>wine explorer
DNG converter is in C:\Program Files (x86)\Adobe\Adobe DNG Converter.exe

How to run DNG converter (GUI)
>wine “C:\Program Files (x86)\Adobe\Adobe DNG Converter.exe”

CLI documentation for DNG convert
https://wwwimages.adobe.com/content/dam/Adobe/en/products/photoshop/pdfs/dng_commandline.pdf

'''