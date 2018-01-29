#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math

class Point:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		
	#From self toward point
	def substract(self, point):
		return Point(point.x - self.x, point.y - self.y)
		
	def dist(self, point):
		vec = self.substract(point)
		dist = (vec.x * vec.x) + (vec.y * vec.y)
		return math.sqrt(dist)
	
class Pose:
	def __init__(self, position = Point(), ori = 0):
		self.position = position
		self.orientation = ori
		
	def getPosition(self):
		return self.position
	def getOrientation(self):
		return self.orientation
	def print(self):
		return str(self.position.x) + " "+ str(self.position.y) + " " + str(self.orientation)


class Data:
	def __init__(self):
		#Tuple with pose and time 
		self.posetime = list()
		self.is_rad = True
		self.convert_to_rad = True
		
	def read(self, file_name, is_radian = True, convert_to_rad = True):
		f = open(file_name, 'r')
		
		self.is_rad = is_radian
		
		for line in f:
			assert len(line.split()) == 4
			orientation = float(line.split()[2])
			if is_radian == False:
				if convert_to_rad == True:
					self.is_rad = True
					orientation = orientation * 2 * math.pi / 360
					#if orientation < 0:
						#orientation = orientation + (2 * math.pi)
					#if orientation >= 2 * math.pi :
						#orientation = orientation - (2 * math.pi)
				#else:
					#if orientation < 0:
						#orientation = orientation + (360)
					#if orientation >= 360 :
						#orientation = orientation - (360)
			##Get all angle between 0 and 2pi
			#else:
				#if orientation < 0:
					#orientation = orientation + (2 * math.pi)
				#if orientation >= 2 * math.pi :
					#orientation = orientation - (2 * math.pi)
			slampose = Pose(Point( float(line.split()[0]), float(line.split()[1] )), orientation)
			self.posetime.append( (slampose, float(line.split()[3]) ) )
			
	def exportGnuplot(self, f):
		#print("El number " + str(len(self.posetime)))
		count = 0
		for el in self.posetime:
			
			#print(str(el[0].position.x) + " " + str(el[0].position.y) + " " + str(el[0].orientation) + " " + str(el[1]) + "\n")
			
			f.write(str(count) + " " + str(el[0].position.x) + " " + str(el[0].position.y) + " " + str(el[0].orientation) + " " + str(el[1]) + "\n")
			count = count + 1
	
	def getPose(self, i):
		return self.posetime[i][0]
	def getTime(self, i):
		return self.posetime[i][1]
	
	#From i toward j
	def getTransDisplacement(self, i, j):
		#print("position " + self.posetime[i][0].print() + " " + self.posetime[j][0].print())
		dist = self.posetime[i][0].getPosition().dist( self.posetime[j][0].getPosition())
		#print("dist " , dist, "position ", self.posetime[i][0].print(), " ", self.posetime[j][0].print())
		return dist
	
	def smallestSignedAngleBetweenRad(self, x, y):
		a = (x - y) % 2 * math.pi
		b = (y - x) % 2 * math.pi
		return -a if a < b else b
	
	def smallestSignedAngleBetweenDeg(self, x, y):
		a = (x - y) % 360
		b = (y - x) % 360
		return -a if a < b else b
	
	#From i toward j
	def getOrientationDisplacement(self, from_i, toward_j):
		if self.is_rad == True:
			return self.smallestSignedAngleBetweenRad(self.posetime[from_i][0].getOrientation(), self.posetime[toward_j][0].getOrientation());
		else:
			return self.smallestSignedAngleBetweenDeg(self.posetime[from_i][0].getOrientation(), self.posetime[toward_j][0].getOrientation());
		
		#diff = self.posetime[from_i][0].getOrientation() - self.posetime[toward_j][0].getOrientation()
		## Get the smallest angle between them
		#if diff > 2 * math.pi:
			#print(diff, " = ", self.posetime[from_i][0].getOrientation(), " - ", self.posetime[toward_j][0].getOrientation() )
		
		#if self.is_rad == True:
			#assert diff >= - math.pi
			#assert diff < math.pi
			
			#if diff > math.pi:
				#diff = (2 * math.pi) - diff
		#else:
			#assert diff >= 0
			#assert diff < 360
			
			#if diff > 180:
				#diff = 360 - diff
		
		#return diff
	
	def visu(self, plot, nb_of_pose = -1, color = 'r'):
		pose_x = list()
		pose_y = list()
		size1 = list()
		if nb_of_pose > len(self.posetime) or nb_of_pose < 0:
			nb_of_pose = len(self.posetime)
		for x in range(0, nb_of_pose):
		#for el in self.posetime:
			pose = self.posetime[x][0]
			pose_x.append(pose.getPosition().x)
			pose_y.append(pose.getPosition().y)
			size1.append(500)
		plot.scatter(pose_x, pose_y, size1, color)
		#maxmin = self.__maxXYminXY()
		#plot.xlim(-4.0, 4.0)
		#plot.xlim(maxmin[2], maxmin[0])
		#plot.ylim(maxmin[3], maxmin[1])

	def __maxXYminXY(self):
		if(len(self.posetime) > 0):
			max_x = self.posetime[0][0].getPosition().x 
			max_y = self.posetime[0][0].getPosition().y
			min_x = self.posetime[0][0].getPosition().x 
			min_y = self.posetime[0][0].getPosition().y 
			for el in self.posetime:
				if(max_x < el[0].getPosition().x):
					max_x = el[0].getPosition().x
				if(max_y < el[0].getPosition().y):
					max_y = el[0].getPosition().y
				if(min_x > el[0].getPosition().x):
					min_x = el[0].getPosition().x
				if(min_y > el[0].getPosition().y):
					min_y = el[0].getPosition().y
			return (max_x, max_y, min_x, min_y)
		else:
			print("EMPTY")
			return (1,1,-1,-1)
		
	def print(self):
		for x in range(0, len(self.posetime)):
			print(str(self.posetime[x][0].getPosition().x) + " " \
				+ str(self.posetime[x][0].getPosition().y) + " " \
				+ str(self.posetime[x][0].getOrientation()) + " " \
				+ str(self.posetime[x][1]))
	
	
