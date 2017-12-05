#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math

from kslamcomp import gnuplot_reader

from kslamcomp import kslamcomp
from kslamcomp import data

class GnuplotReducer():
    def __init__(self, file_base, file_toupdate):
        self.reader_base
        self.reader_toupdate
        self.reader_base.read(file_base)
        self.reader_toupdate.read(file_toupdate)
        
        self.base 
        self.toupdate
        
        #SlamData()
        #GTData()
        
    #def SlamData(self):
        #pass
    
    #def GTData(self):
        #pass
    
    def sortSLAM(self, delta = 0):
		self.base = []
		self.toupdate = []
		
		seen = list()
		seen_slam = list() # to avoid double value when rounding the time in the result file
		
		for element in self.reader_base.posetime_slam:
			#print("new element " + element[0].print() + " time " + str(element[1]))
			seen_slam_time = any(slam_time == element[1] for slam_time in seen_slam)
			#for slam_times in seen_slam:
				#if (element[1] == slam_times):
					#seen_slam_time = True
			if seen_slam_time == False:
				toadd = list()
				for el_gt in self.reader_toupdate.posetime_slam:
					#print("checking" + str(element[1]) + " "+ str(el_gt[1]))
					if element[1] <= el_gt[1] + delta and element[1] >= el_gt[1] - delta:
						seen_b = False
						for times in seen:
							if(el_gt[1] == times):
								seen_b = True
						if(seen_b == False):
							#Keep the one with the closest time
							if len(toadd) == 2:
								if abs(toadd[1][1] - element[1]) > abs(el_gt[1] - element[1]):
									toadd = []
									toadd.append(element)
									toadd.append(el_gt)
							else:
								toadd = []
								toadd.append(element)
								toadd.append(el_gt)
				if len(toadd) == 2:
					seen.append(toadd[1][1])
					self.slam.append(toadd[1])
				seen_slam.append(element[1])
			
		assert len(self.slam.posetime) == len(self.gt.posetime)
		
		for x in range(0, len(self.slam.posetime)):
			for x2 in range(x + 1, len(self.slam.posetime)):
				if self.slam.posetime[x][1] == self.slam.posetime[x2][1]:
					print("Repeating SLAM value: ", x, " and ", x2, "with ", self.slam.posetime[x][1], " == ", self.slam.posetime[x2][1])
					return False
					
		for x in range(0, len(self.gt.posetime)):
			for x2 in range(x + 1, len(self.gt.posetime)):
				if self.gt.posetime[x][1] == self.gt.posetime[x2][1]:
					print("Repeating GT value")
					return False
		
		return True
