#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from kslamcomp import data
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class KSlamComp:
	def __init__(self, forward_nodes_lookup = 1, backward_nodes_lookup = 0, slam_input_raw = None, gt_input_raw = None):
		self.slam_raw = slam_input_raw or data.Data()
		self.gt_raw = gt_input_raw or data.Data()
		self.slam = data.Data()
		self.gt = data.Data()
		self.nb_node_forward = forward_nodes_lookup
		self.nb_node_backward = backward_nodes_lookup
	
	def read(self, file_name):
		assert(len(self.slam_raw.posetime) == 0)
		f = open(file_name, 'r')
		for line in f:
			#print("line")
			assert len(line.split()) == 8
			
			slampose = data.Pose(data.Point( float(line.split()[0]), float(line.split()[1] )),  float(line.split()[2]))
			gtpose = data.Pose(data.Point( float(line.split()[4]), float(line.split()[5] )),  float(line.split()[6]))
			
			self.slam_raw.posetime.append( (slampose, float(line.split()[3]) ) )
			self.gt_raw.posetime.append( (gtpose, float(line.split()[7]) ) )
			
	def readSLAM(self, slam_file_name, gt_file_name):
		self.slam_raw.read(slam_file_name)
		self.gt_raw.read(gt_file_name)
		#assert len(self.slam_raw.posetime) == len(self.gt_raw.posetime)
			
	def readSLAM(self, file_name):
		self.slam_raw.read(file_name)
			
	def readGT(self, file_name):
		self.gt_raw.read(file_name)
	
	def print(self):
		print("Printing data")
		print("SLAM")
		for x in range(0, len(self.slam.posetime)):
			print(str(self.slam.posetime[x][0].getPosition().x) + " " \
				+ str(self.slam.posetime[x][0].getPosition().y) + " " \
				+ str(self.slam.posetime[x][0].getOrientation()) + " " \
				+ str(self.slam.posetime[x][1]))
		print("GT")
		for x in range(0, len(self.gt.posetime)):
			print(str(self.gt.posetime[x][0].getPosition().x) + " " \
				+ str(self.gt.posetime[x][0].getPosition().y) + " " \
				+ str(self.gt.posetime[x][0].getOrientation()) + " " \
				+ str(self.gt.posetime[x][1]))
		print("\n")
			
	def printraw(self):
		print("Printing Raw data")
		print("SLAM Raw")
		for x in range(0, len(self.slam_raw.posetime)):
			print(str(self.slam_raw.posetime[x][0].getPosition().x) + " " \
				+ str(self.slam_raw.posetime[x][0].getPosition().y) + " " \
				+ str(self.slam_raw.posetime[x][0].getOrientation()) + " " \
				+ str(self.slam_raw.posetime[x][1]))
		print("GT Raw")
		for x in range(0, len(self.gt_raw.posetime)):
			print(str(self.gt_raw.posetime[x][0].getPosition().x) + " " \
				+ str(self.gt_raw.posetime[x][0].getPosition().y) + " " \
				+ str(self.gt_raw.posetime[x][0].getOrientation()) + " " \
				+ str(self.gt_raw.posetime[x][1]))
		print("\n")
	
	def getSLAMsize(self):
		return len(self.slam.posetime)

	def compute(self, nb_of_pose = -1):
		"""
		Compute the total error in the SLAM. Don't forget to call sort before
		"""
		
		displacement = 0
		#print(len(self.slam.posetime))
		if nb_of_pose > len(self.slam.posetime) or nb_of_pose < 0:
			nb_of_pose = len(self.slam.posetime)
		for x in range(0, nb_of_pose):
			displacement = displacement + self.computeDisplacementNode(x, x)
		return displacement
	
	def visu(self, nb_of_pose = -1):
		if nb_of_pose > len(self.slam.posetime) or nb_of_pose < 0:
			nb_of_pose = len(self.slam.posetime)
		plt.figure(1)
		self.slam.visu(plt, nb_of_pose)
		plt.title("slam")
		plt.figure(2)
		self.gt.visu(plt, nb_of_pose)
		plt.title("gt")
		
		#plt.figure(3)
		#self.slam_raw.visu(plt, nb_of_pose)
		#plt.title("slam raw")
		#plt.figure(4)
		#self.gt_raw.visu(plt, nb_of_pose)
		#plt.title("gtraw")
		plt.show(block=False)
	
	#Protected functions
	
	def sort(self, delta = 0):
		self.slam.posetime = []
		self.gt.posetime = []
		
		seen = list()
		
		for element in self.slam_raw.posetime:
			#print("new element " + element[0].print() + " time " + str(element[1]))
			toadd = list()
			for el_gt in self.gt_raw.posetime:
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
				self.slam.posetime.append(toadd[0])
				self.gt.posetime.append(toadd[1])
		assert len(self.slam.posetime) == len(self.gt.posetime)
		
		for x in range(0, len(self.slam.posetime)):
			for x2 in range(x + 1, len(self.slam.posetime)):
				if self.slam.posetime[x][1] == self.slam.posetime[x2][1]:
					print("Repeating SLAM value")
					return False
					
		for x in range(0, len(self.gt.posetime)):
			for x2 in range(x + 1, len(self.gt.posetime)):
				if self.gt.posetime[x][1] == self.gt.posetime[x2][1]:
					print("Repeating GT value")
					return False
		
		return True
		
	
	
	def computeDisplacementNode(self, i_slam, i_gt):
		"""
		Compute the displacement between two nodes i_slam and i_gt
		"""
		displacement = 0
		node_forward_slam = i_slam
		node_forward_gt = i_gt
		slamposition_init = self.slam.getPose(i_slam).getPosition()
		
		#print("UP")
		while node_forward_slam - i_slam <= self.nb_node_forward and node_forward_slam < len(self.slam.posetime):
			#Trans displacement 
			transdist_slam = self.slam.getTransDisplacement(i_slam, node_forward_slam)
			transdist_gt = self.gt.getTransDisplacement(i_gt, node_forward_gt)
			transnoise = (transdist_gt - transdist_slam) * (transdist_gt - transdist_slam)
			
			#print("trans noise " + str(transnoise))
			
			displacement = displacement + transnoise
			
			#Rot displacement
			oriendist_slam = self.slam.getOrientationDisplacement(i_slam, node_forward_slam)
			oriendist_gt = self.gt.getOrientationDisplacement(i_gt, node_forward_gt)
			orientnoise = (oriendist_slam - oriendist_gt) * (oriendist_slam - oriendist_gt)
			 
			displacement = displacement + orientnoise
			
			node_forward_gt = node_forward_gt + 1
			node_forward_slam = node_forward_slam + 1
		
		
		#print("DOWN")
		node_backward_slam = i_slam
		node_backward_gt = i_gt
		
		while i_slam - node_backward_slam  <= self.nb_node_backward and node_backward_slam >= 0:
			#Trans displacement 
			transdist_slam = self.slam.getTransDisplacement(i_slam, node_backward_slam)
			transdist_gt = self.gt.getTransDisplacement(i_gt, node_backward_gt)
			transnoise = (transdist_gt - transdist_slam) * (transdist_gt - transdist_slam)
			
			#print("trans noise " + str(transnoise))
			
			displacement = displacement + transnoise
			
			#Rot displacement
			oriendist_slam = self.slam.getOrientationDisplacement(i_slam, node_backward_slam)
			oriendist_gt = self.gt.getOrientationDisplacement(i_gt, node_backward_gt)
			orientnoise = (oriendist_slam - oriendist_gt) * (oriendist_slam - oriendist_gt)
			 
			displacement = displacement + orientnoise

			node_backward_gt = node_backward_gt - 1
			node_backward_slam = node_backward_slam - 1
			
		return displacement
	
