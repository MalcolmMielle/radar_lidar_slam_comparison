#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math

from kslamcomp import data
import warnings
from kslamcomp import kslamcomp

class GmappingMaker:
    def __init__(self):
        self.time = list()
        self.posetime_slam = data.Data()
        self.toupdate = data.Data()
    
    def readTimes(self, file_name):
        f = open(file_name, 'r')
        for line in f:
            if(len(line) > 1):
                self.time.append(float(line.split()[0]) )
                
    def writeSLAM(self, file_out):
        self.toupdate.write(file_out)
    
    def mean_time(self):
        sum = 0
        for el in self.time:
            sum = sum + el
        return sum / len(self.time)
    
    def readSLAM(self, file_name, min_diff_in_pose = -1, is_radian = True, cov_rad = False):
        self.posetime_slam.read(file_name, min_diff_in_pose, is_radian, cov_rad)

    
    def reduce(self, delta = 0):
        to_update_kslamcomp = kslamcomp.KSlamComp()
        indexes = self.reduceSLAM(delta)
        to_update_kslamcomp.slam_raw = self.toupdate
        assert len(to_update_kslamcomp.slam_raw.posetime) == len(to_update_kslamcomp.gt_raw.posetime)
        return to_update_kslamcomp
    
    def reduceSLAM(self, delta = 0):
        #self.toupdate = []

        indexes = list()

        seen = list()
        seen_slam = list() # to avoid double value when rounding the time in the result file

        print(len(self.posetime_slam.posetime))

        for element in self.time:
            #print("new element " + element[0].print() + " time " + str(element[1]))
            seen_slam_time = any(slam_time == element for slam_time in seen_slam)
            #for slam_times in seen_slam:
            #if (element[1] == slam_times):
            #seen_slam_time = True
            if seen_slam_time == False:
                toadd = list()
                index = -1
                count = 0
                for sl_slam in self.posetime_slam.posetime:
                    #print("checking" + str(element[1]) + " "+ str(sl_slam[1]))
                    if element <= sl_slam[1] + delta and element >= sl_slam[1] - delta:
                        seen_b = False
                        for times in seen:
                            if(sl_slam[1] == times):
                                seen_b = True
                        if(seen_b == False):
                            #Keep the one with the closest time
                            if len(toadd) == 2:
                                if abs(toadd[1][1] - element) > abs(sl_slam[1] - element):
                                    toadd = []
                                    toadd.append(element)
                                    toadd.append(sl_slam)
                                    index = count
                            else:
                                toadd = []
                                toadd.append(element)
                                toadd.append(sl_slam)
                                index = count
                    count= count + 1
                if len(toadd) == 2:
                    seen.append(toadd[1][1])
                    self.toupdate.posetime.append(toadd[1])
                    assert index != -1
                    indexes.append(index)
                seen_slam.append(element)

        for x in range(0, len(self.toupdate.posetime)):
            for x2 in range(x + 1, len(self.toupdate.posetime)):
                if self.toupdate.posetime[x][1] == self.toupdate.posetime[x2][1]:
                    print("Repeating SLAM value: ", x, " and ", x2, "with ", self.toupdate.posetime[x][1], " == ", self.toupdate.posetime[x2][1])
                    return False

        print(len(indexes), "==" ,len(self.time))

        if (len(indexes) != len(self.time)):
            warnings.warn("The instance will not have the same size")

        return indexes

def main():
    
    
    #People long
    gmappingmaker = GmappingMaker()
    gmappingmaker.readSLAM("data_files/GMapping/Updates/people_long_gmapping_mpr.txt")
    gmappingmaker.readTimes("data_files/GMapping/Updates/people_long_gmapping_mpr_update_times.txt")
    gmappingmaker.reduceSLAM(0.5)
    gmappingmaker.writeSLAM("data_files/GMapping/Updates/people_long_gmapping_mpr_reduced.txt")
    
    
    gmappingmakerlaser = GmappingMaker()
    gmappingmakerlaser.readSLAM("data_files/GMapping/Updates/people_long_gmapping_laser.txt")
    gmappingmakerlaser.readTimes("data_files/GMapping/Updates/people_long_gmapping_laser_update_times.txt")
    gmappingmakerlaser.reduceSLAM(0.5)
    gmappingmakerlaser.writeSLAM("data_files/GMapping/Updates/people_long_gmapping_laser_reduced.txt")
    
    #30
    gmappingmakerlaser30 = GmappingMaker()
    gmappingmakerlaser30.readSLAM("data_files/GMapping/Updates/2017-08-29-15-30-59_gmapping_laser.txt")
    gmappingmakerlaser30.readTimes("data_files/GMapping/Updates/2017-08-29-15-30-59_gmapping_laser_update_times.txt")
    gmappingmakerlaser30.reduceSLAM(0.5)
    gmappingmakerlaser30.writeSLAM("data_files/GMapping/Updates/2017-08-29-15-30-59_gmapping_laser_reduced.txt")
    
    gmappingmakermpr30 = GmappingMaker()
    gmappingmakermpr30.readSLAM("data_files/GMapping/Updates/2017-08-29-15-30-59_gmapping_mpr.txt")
    gmappingmakermpr30.readTimes("data_files/GMapping/Updates/2017-08-29-15-30-59_gmapping_mpr_update_times.txt")
    gmappingmakermpr30.reduceSLAM(0.5)
    gmappingmakermpr30.writeSLAM("data_files/GMapping/Updates/2017-08-29-15-30-59_gmapping_mpr_reduced.txt")
    
    #37
    gmappingmakerlaser37 = GmappingMaker()
    gmappingmakerlaser37.readSLAM("data_files/GMapping/Updates/2017-08-29-15-37-08_gmapping_laser.txt")
    gmappingmakerlaser37.readTimes("data_files/GMapping/Updates/2017-08-29-15-37-08_gmapping_laser_update_times.txt")
    gmappingmakerlaser37.reduceSLAM(0.5)
    gmappingmakerlaser37.writeSLAM("data_files/GMapping/Updates/2017-08-29-15-37-08_gmapping_laser_reduced.txt")
    
    
    gmappingmakermpr37 = GmappingMaker()
    gmappingmakermpr37.readSLAM("data_files/GMapping/Updates/2017-08-29-15-37-08_gmapping_mpr.txt")
    gmappingmakermpr37.readTimes("data_files/GMapping/Updates/2017-08-29-15-37-08_gmapping_mpr_update_times.txt")
    gmappingmakermpr37.reduceSLAM(0.5)
    gmappingmakermpr37.writeSLAM("data_files/GMapping/Updates/2017-08-29-15-37-08_gmapping_mpr_reduced.txt")


if __name__ == "__main__":
    main()
