#! /usr/bin/python
"""
This script reads experimenatal and simulated
layer lines and convets them to an iamge

Usage: layerLinesToImage.py -e layer_lines(experimental) -s layer_lines(simulated)

layer_lines - text file containing containing three columns 1st: Intensity,
2nd reciprocal Rs, 3rd: Number of Layer line

"""
__author__ = "Wojtek Potrzebowski"
__maintainer__ = "Wojtek Potrzebowski"
__email__ = "Wojciech.Potrzebowski@biochemistry.lu.se"

import optparse
import os
import sys 
import numpy as np
import matplotlib.pyplot as plt


def read_layer_lines(filename, simulated=False):
	f = open(filename)
	R_l = {}
	I_l = {}
	lines = f.readlines()
	for line in lines:
		line_arr = line.split(" ")
		layer_index = int(line_arr[2].strip())
		reciprocal_R = float(line_arr[1])
		if simulated:
			intensity = np.sqrt(float(line_arr[0]))
		else:
			intensity = float(line_arr[0])
		if layer_index in R_l:
			R_l[layer_index].append(reciprocal_R)
			I_l[layer_index].append(intensity)
		else:
			R_l[layer_index] = [reciprocal_R]
			I_l[layer_index] = [intensity]
	return R_l, I_l


def convert_to_image(ExpR, ExpI, SimR, SimI, output): #modded to add output
	"""
	Makes plots from layer lines and store them in image file
	"""
	layer_lines_no = len(ExpR.keys())
	fig, axrr = plt.subplots(nrows=layer_lines_no)

	lindex = 0 #Should be the same as layer line but better play safe
	for lline in ExpR.keys():
		#And will have add simulated stuff as well
		axrr[lindex].plot(ExpR[lline], ExpI[lline])
		axrr[lindex].plot(SimR[lline], SimI[lline])
		axrr[lindex].set_yticklabels([])
		lindex+=1

	# Only show ticks on the left and bottom spines
	#ax1.yaxis.set_ticks_position('left')
	#ax1.xaxis.set_ticks_position('bottom')

	# Tweak spacing between subplots to prevent labels from overlapping
	plt.subplots_adjust(hspace=0.5)
	plt.savefig(output)#modded to add output
	#plt.show()   #modded to avoid showing


if __name__=="__main__":
	doc = """
	    Reads simulated and experimental layer lines from input files
	    and converts it to image.
	    Usage: python layerLinesToImage.py --help
	"""
	#print doc
	usage = "usage: %prog [options] args"
	option_parser_class = optparse.OptionParser
	parser = option_parser_class( usage = usage, version='0.1' )

	parser.add_option("-e", "--experimental", dest="experimental",
                      help="Experimental layer lines [OBLIGATORY]")
	parser.add_option("-s", "--simulated", dest="simulated",
                      help="Simulated layer lines [OBLIGATORY]")

	#modded to add output flag (makes LLoutputpic)
	parser.add_option("-o", "--output", dest="output",
                      help="output [OBLIGATORY]")

	options, args = parser.parse_args()
	experimental = options.experimental
	simulated = options.simulated
	output = options.output  #modded to add output

	ExpR, ExpI = read_layer_lines(experimental)
	SimR, SimI = read_layer_lines(simulated, True)

	convert_to_image(ExpR,ExpI,SimR,SimI,output)  #modded to add output