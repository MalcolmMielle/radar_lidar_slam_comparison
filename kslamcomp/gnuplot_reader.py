#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math

from data import Pose

class GnuplotReader:
    def __init__(self):
        self.posetime_slam = list()
        self.posetime_gt = list()
        self.displacement = list()
        self.sum = list()
    
    def read(self, file_name):
        f = open(file_name, 'r')
        step = 0
        for line in f:
            first_letter = line.split(None, 1)[0]
            if first_letter == "#" :
                step = step + 1
            if step == 1:
                readTrajSLAm(line)
            elif step == 2:
                readTrajGT(line)
            elif step == 3:
                readDisplacement(line)
                
    
    def readTrajSLAM(self, line):
        slampose = data.Pose(Point( float(line.split()[0]), float(line.split()[1] )),  float(line.split()[2]))
        self.posetime_slam.append( (slampose, float(line.split()[3]) ) )
    
    def readTrajGT(self, line):
        slampose = data.Pose(Point( float(line.split()[0]), float(line.split()[1] )),  float(line.split()[2]))
        self.posetime_gt.append( (slampose, float(line.split()[3]) ) )
        
    
    def readDisplacement(self, line):
        self.displacement.append(float(line.split()[0]))
        self.sum.append(float(line.split()[1] ))
