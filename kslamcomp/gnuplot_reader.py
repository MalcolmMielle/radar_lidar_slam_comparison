#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math

from kslamcomp import data

class GnuplotReader:
    def __init__(self):
        self.posetime_slam = data.Data()
        self.posetime_gt = data.Data()
        self.displacement = list()
        self.sum = list()
        self.time = list()
        self.displacement_abs = list()
        self.sum_abs = list()
        self.time_abs = list()
     
    def print(self):
        print("SLAM raw")
        self.posetime_slam.print()

    def readTrajSLAM(self, line):
        slampose = data.Pose(data.Point( float(line.split()[1]), float(line.split()[2] )),  float(line.split()[3]))
        self.posetime_slam.posetime.append( (slampose, float(line.split()[4]) ) )
    
    def readTrajGT(self, line):
        slampose = data.Pose(data.Point( float(line.split()[1]), float(line.split()[2] )),  float(line.split()[3]))
        self.posetime_gt.posetime.append( (slampose, float(line.split()[4]) ) )
        
    
    def readDisplacement(self, line):
        self.displacement.append(float(line.split()[1]))
        self.sum.append(float(line.split()[2] ))
        self.time.append(float(line.split()[3] ))
        
    def readDisplacementAbs(self, line):
        self.displacement_abs.append(float(line.split()[1]))
        self.sum_abs.append(float(line.split()[2] ))
        self.time_abs.append(float(line.split()[3] ))
    
    def read(self, file_name):
        f = open(file_name, 'r')
        step = 0
        for line in f:
            #print(len(line))
            if(len(line) > 1):
                #print(line)
                first_letter = line.split(None, 1)[0]
                #print(first_letter)
                if first_letter == "#" :
                    step = step + 1
                elif step == 1:
                    self.readTrajSLAM(line)
                elif step == 2:
                    self.readTrajGT(line)
                elif step == 3:
                    self.readDisplacement(line)
                elif step == 4:
                    self.readDisplacementAbs(line)
                
    
    
