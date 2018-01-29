#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math

from kslamcomp import gnuplot_reader

from kslamcomp import kslamcomp
from kslamcomp import data

import warnings

class GnuplotReducer:
	def __init__(self, file_base, file_toupdate):
		self.reader_base = gnuplot_reader.GnuplotReader()
		self.reader_toupdate = gnuplot_reader.GnuplotReader()
		self.reader_base.read(file_base)
		self.reader_toupdate.read(file_toupdate)
		
		#self.base 
		self.toupdate = data.Data()
		#self.displacement = list()
		#self.sum = list()
		#self.displacement_abs = list()
		#self.sum_abs = list()
		
	#def exportGnuplot(self, file_out):
		#f = open(file_out, 'w')
		#f.write("# SLAM - pose_x pose_y orientation time" + "\n")
		#self.toupdate.exportGnuplot(f)
		#f.write("\n\n# GT - pose_x pose_y orientation time" + "\n")
		#self.reader_toupdate.posetime_gt.exportGnuplot(f)
		#count = 0
		#f.write("\n\n# Displacement and sum" + "\n")
		#for el in self.displacement:
			#f.write(str(count) + " " + str(el)+ " " + str(self.sum[count]) + "\n")
			#count = count + 1
		#f.write("\n\n# Displacement absolute and sum" + "\n")
		#count = 0
		#for el in self.displacement_abs:
			#f.write(str(count) + " " + str(el)+ " " + str(self.sum_abs[count]) + "\n")
			#count = count + 1

	#def print(self):
		#print("Reader base")
		#self.reader_base.print()
		#print("Reader to update")
		#self.reader_toupdate.print()
	
	#def printReducedSLAM(self):
		#print("REDUCED SLAM")
		#self.toupdate.print()
		#print("DISPLACEMENT")
		#for i in range(len(self.displacement)):
			#print(i, " ", self.displacement[i], " ", self.sum[i])
	#SlamData()
	#GTData()

	#def SlamData(self):
	#pass

	#def GTData(self):
	#pass
	def reduce(self, delta = 0):
		
		to_update_kslamcomp = kslamcomp.KSlamComp()
		
		indexes = self.reduceSLAM(delta)
		
		to_update_kslamcomp.slam_raw = self.toupdate
		for el in indexes:
			to_update_kslamcomp.gt_raw.posetime.append( self.reader_toupdate.posetime_gt.posetime[el] )
		
		assert len(to_update_kslamcomp.slam_raw.posetime) == len(to_update_kslamcomp.gt_raw.posetime)
		
		return to_update_kslamcomp
		
		#for el in indexes:
			##print(el, " sum ", self.reader_toupdate.sum[el])
			#self.displacement.append(self.reader_toupdate.displacement[el])
			#self.sum.append(self.reader_toupdate.sum[el])
			#self.displacement_abs.append(self.reader_toupdate.displacement_abs[el])
			#self.sum_abs.append(self.reader_toupdate.sum_abs[el])
	

	def reduceSLAM(self, delta = 0):
		#self.toupdate = []
		
		indexes = list()
		
		seen = list()
		seen_slam = list() # to avoid double value when rounding the time in the result file
		
		print(len(self.reader_base.posetime_slam.posetime))
		
		for element in self.reader_base.posetime_slam.posetime:
			#print("new element " + element[0].print() + " time " + str(element[1]))
			seen_slam_time = any(slam_time == element[1] for slam_time in seen_slam)
			#for slam_times in seen_slam:
				#if (element[1] == slam_times):
					#seen_slam_time = True
			if seen_slam_time == False:
				toadd = list()
				index = -1
				count = 0
				for el_gt in self.reader_toupdate.posetime_slam.posetime:
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
									index = count
							else:
								toadd = []
								toadd.append(element)
								toadd.append(el_gt)
								index = count
					count= count + 1
				if len(toadd) == 2:
					seen.append(toadd[1][1])
					self.toupdate.posetime.append(toadd[1])
					assert index != -1
					indexes.append(index)
				seen_slam.append(element[1])
					
		for x in range(0, len(self.toupdate.posetime)):
			for x2 in range(x + 1, len(self.toupdate.posetime)):
				if self.toupdate.posetime[x][1] == self.toupdate.posetime[x2][1]:
					print("Repeating SLAM value: ", x, " and ", x2, "with ", self.toupdate.posetime[x][1], " == ", self.toupdate.posetime[x2][1])
					return False
				
		print(len(indexes), "==" ,len(self.reader_base.posetime_slam.posetime))
		
		if (len(indexes) != len(self.reader_base.posetime_slam.posetime)):
			warnings.warn("The instance will not have the same size")
		
		return indexes
