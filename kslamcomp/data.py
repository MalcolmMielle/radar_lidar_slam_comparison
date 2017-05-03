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
		
	def read(self, file_name):
		f = open(file_name, 'r')
		for line in f:
			assert len(line.split()) == 4
			slampose = Pose(Point( float(line.split()[0]), float(line.split()[1] )),  float(line.split()[2]))
			self.posetime.append( (slampose, float(line.split()[3]) ) )
	
	def getPose(self, i):
		return self.posetime[i][0]
	def getTime(self, i):
		return self.posetime[i][1]
	
	#From i toward j
	def getTransDisplacement(self, i, j):
		#print("position " + self.posetime[i][0].print() + " " + self.posetime[j][0].print())
		dist = self.posetime[i][0].getPosition().dist( self.posetime[j][0].getPosition())
		#print("dist " + str(dist))
		return dist
	
	#From i toward j
	def getOrientationDisplacement(self, from_i, toward_j):
		diff = self.posetime[from_i][0].getOrientation() - self.posetime[toward_j][0].getOrientation()
		while diff < 0 :
			diff = diff + (2 * math.pi)
		while diff > 2 * math.pi :
			diff = diff - (2 * math.pi)
		return diff
