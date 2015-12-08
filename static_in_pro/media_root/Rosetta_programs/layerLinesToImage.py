#! /usr/bin/python
"""
This script reads experimenatal and experimental
layer lines and convets them to an iamge

Usage: layerLinesToImage.py -e layer_lines(experimental) -s layer_lines(experimental)

layer_lines - text file containing containing three columns 1st: Intensity,
2nd reciprocal Rs, 3rd: Number of Layer line

"""
__author__ = "Wojtek Potrzebowski, modded by Stephen Burleigh"
__maintainer__ = "Wojtek Potrzebowski"
__email__ = "Wojciech.Potrzebowski@biochemistry.lu.se"

import optparse
import numpy as np
import matplotlib
from matplotlib.pyplot import xlabel, ylabel, title
matplotlib.use('Agg')  #!main thread is not in main loop error if not included
import matplotlib.pyplot as plt             #this removes the previous plot from main thread
from trydjango18.views import Sound

class LLTI(object):
    """ class to run LLtoImage, avoid 'main thread is not in main loop' error"""
    def __init__(self, intensity, experimental, output, runnum):
        self.ExpR = {}
        self.ExpI = {}
        self.SimR = {}
        self.SimI = {}
        self.intensity = intensity
        self.experimental = experimental
        self.output = output
        self.runnum = runnum

        if 'none chosen' in str(self.experimental):
            self.SimR, self.SimI = self.read_layer_lines(self.intensity, True)
            self.ExpR, self.ExpI = self.read_layer_lines(self.intensity, True)
        else:
            self.SimR, self.SimI = self.read_layer_lines(self.intensity, True)
            self.ExpR, self.ExpI = self.read_layer_lines(self.experimental)

    def read_layer_lines(self, theFile, Sim=False):
        path='static_in_pro/media_root/' + theFile
        f = open(path)
        R_l = {}
        I_l = {}
        lines = f.readlines()
        for line in lines:
            line_arr = line.split()
            layer_index = int(line_arr[2].strip())
            reciprocal_R = float(line_arr[1])
            if Sim:
                intensity = np.sqrt(float(line_arr[0]))
            else:
                 intensity = float(line_arr[0])
                
            if layer_index in R_l:
                R_l[layer_index].append(reciprocal_R)
                I_l[layer_index].append(intensity)
            else:
                R_l[layer_index] = [reciprocal_R]
                I_l[layer_index] = [intensity]
            self.layerlines_no=layer_index
        return R_l, I_l

    def convert_to_image(self, runnum): #modded to add output
        from matplotlib.backends.backend_agg import FigureCanvasAgg
        """
        Makes plots from layer lines and store them in image file
        """
        layer_lines_no = int(self.layerlines_no)
        fig, axrr = plt.subplots(nrows=layer_lines_no+1)
        mytitle = 'Layer-Lines plot for Run' + str(runnum) + "\n" + 'Green: simulated; Blue; experimental (if provided)'
        fig.suptitle(mytitle)
        
        lindex = 0 #Should be the same as layer line but better play safe
        count = 1 #stop x axis from printing, until bottom
        for lline in self.ExpR.keys():
            #And will have add experimental stuff as well
            axrr[lindex].plot(self.ExpR[lline], self.ExpI[lline])
            axrr[lindex].plot(self.SimR[lline], self.SimI[lline])
            axrr[lindex].set_yticklabels([])
            if count < len(self.ExpR):
                axrr[lindex].set_xticklabels([])
            lindex+=1
            count = count + 1
            plt.tick_params(axis='both', which='major', labelsize=8)
            #plt.tick_params(axis='both', which='minor', labelsize=6)
        #plt.subplots_adjust(hspace=0.5)# Tweak spacing between subplots to prevent labels from overlapping
        plt.xlabel('Reciprocal (1/Å)')
        plt.ylabel("                                                                          Intensity")     
        
        plt.subplots_adjust(hspace=0.5)
        fig.savefig(self.output)
