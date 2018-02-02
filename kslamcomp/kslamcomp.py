#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from kslamcomp import data
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class KSlamComp:
    def __init__(self, forward_nodes_lookup = 1, backward_nodes_lookup = 0, slam_input_raw = None, gt_input_raw = None):
        self.slam_raw = slam_input_raw or data.Data()
        self.gt_raw = gt_input_raw or data.Data()
        self.slam = data.Data()
        self.gt = data.Data()
        self.nb_node_forward = forward_nodes_lookup
        self.nb_node_backward = backward_nodes_lookup
        self.displacement_vec = list()
        self.displacement_vec_abs = list()
        self.distance_slam_gt = list()
        
        self.use_orientation = False
        self.use_translation = True
        
        self.mean_displacement = -1
        self.std_deviation = -1
        self.mean_displacement_abs = -1
        self.std_deviation_abs = -1
        self.mean_distance_gt = -1
        self.mean_distance_gt_sd = -1
        
        self.distance_to_gt = -1

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
            
    def readSLAM(self, file_name, is_radian = True, cov_rad = False):
        self.slam_raw.read(file_name, is_radian, cov_rad)
            
    def readGT(self, file_name, is_radian = True, cov_rad = False):
        self.gt_raw.read(file_name, is_radian, cov_rad)

    def print(self):
        print("Printing data")
        print("SLAM")
        self.slam.print()
        
        print("GT")
        self.gt.print()

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
        
    def printDisplacement(self):
        sum = 0
        for x in range(self.nb_node_backward, len(self.slam.posetime) - self.nb_node_forward):
            print(str(self.displacement_vec[x]) + " at " + str(self.slam.posetime[x][0].getPosition().x))
            sum = sum + self.displacement_vec[x]
        print("\n")
        print(sum)

    def getSLAMsize(self):
        return len(self.slam.posetime)

    def compute(self, nb_of_pose = -1, squared = True):
        """
        Compute the total error in the SLAM. Don't forget to call sort before
        """
        self.displacement_vec.clear()
        self.displacement_vec_abs.clear()
        displacement = 0
        displacement_abs = 0
        #print(len(self.slam.posetime))
        if nb_of_pose > len(self.slam.posetime) or nb_of_pose < 0:
            nb_of_pose = len(self.slam.posetime)
        for x in range(0, nb_of_pose):
            #print(x, "of", nb_of_pose)
            displacement_here = self.computeDisplacementNode(x, x, squared)
            #print(displacement)
            displacement = displacement + displacement_here[0]
            displacement_abs = displacement_abs + displacement_here[1]
            self.displacement_vec.append(displacement_here[0])
            self.displacement_vec_abs.append(displacement_here[1])
            
        self.compute_distance_to_gt()
        
        return (displacement, displacement_abs)

    def exportGnuplot(self, file_out):
        f = open(file_out, 'w')
        f.write("# SLAM - pose_x pose_y orientation time" + "\n")
        self.slam.exportGnuplot(f)
        
        f.write("\n\n# GT - pose_x pose_y orientation time" + "\n")
        self.gt.exportGnuplot(f)
        
        f.write("\n\n# Displacement and sum" + "\n")
        sum = 0
        count = 0
        for el in self.displacement_vec:
            sum = sum + el
            f.write(str(count) + " " + str(el)+ " " + str(sum) + "\n")
            count = count + 1
            
        f.write("\n\n# Displacement abs and sum" + "\n")
        sum = 0
        count = 0
        for el in self.displacement_vec_abs:
            sum = sum + el
            f.write(str(count) + " " + str(el)+ " " + str(sum) + "\n")
            count = count + 1
            
        f.write("\n\n# Distance slam gt" + "\n")
        count = 0
        for el in self.distance_slam_gt:
            f.write(str(count) + " " + str(el)+ "\n")
            count = count + 1
        
        f.write("\n\n# Displacement mean and std deviation" + "\n")
        f.write(str(self.mean_displacement) + " " + str(self.std_deviation) )
        
        f.write("\n\n# Displacement mean absolute value and std deviation" + "\n")
        f.write(str(self.mean_displacement_abs) + " " + str(self.std_deviation_abs) )
        
        f.write("\n\n# Distance to GT" + "\n")
        f.write(str(self.distance_to_gt) )
        
        f.close()
        
    def add_to_dictionnary(self, suffix, dict):
        
        round_up = lambda num : math.ceil(num * 1000) / 1000
        
        name = "d_" + suffix 
        dict[name] = round_up(self.distance_to_gt)
        if self.use_translation == True:
            name = "dp_" + suffix 
            dict[name] = round_up(self.mean_displacement_abs)
            name = "dpsd_" + suffix 
            dict[name] = round_up(self.std_deviation_abs)
        else:
            name = "do_" + suffix 
            dict[name] = round_up(self.mean_displacement_abs)
            name = "dosd_" + suffix 
            dict[name] = round_up(self.std_deviation_abs)
        name = "dgt_" + suffix
        dict[name] = round_up(self.mean_distance_gt)
        name = "dgtsd_" + suffix
        dict[name] = round_up(self.mean_distance_gt_sd)
        
            
    def visuSLAM(self, nb_of_pose = -1, block = False):
        if nb_of_pose > len(self.slam.posetime) or nb_of_pose < 0:
            nb_of_pose = len(self.slam.posetime)
        plt.figure(1)
        self.slam.visu(plt, nb_of_pose)
        plt.title("slam")
        
    def visuSLAMRaw(self, nb_of_pose = -1, block = False):
        print("print raw")
        if nb_of_pose > len(self.slam_raw.posetime) or nb_of_pose < 0:
            nb_of_pose = len(self.slam_raw.posetime)
        plt.figure(1)
        self.slam_raw.visu(plt, nb_of_pose)
        plt.title("slam")

    def visuGT(self, nb_of_pose = -1, block = False):
        if nb_of_pose > len(self.gt.posetime) or nb_of_pose < 0:
            nb_of_pose = len(self.gt.posetime)
        #plt.figure(2)
        self.gt.visu(plt, nb_of_pose, 'b')
        plt.title("gt")


    def visu(self, nb_of_pose = -1, block = False):
        self.visuSLAM(nb_of_pose, block)
        self.visuGT(nb_of_pose, block)
        #if nb_of_pose > len(self.slam.posetime) or nb_of_pose < 0:
            #nb_of_pose = len(self.slam.posetime)
        #plt.figure(1)
        #self.slam.visu(plt, nb_of_pose)
        #plt.title("slam")
        ##plt.figure(2)
        #self.gt.visu(plt, nb_of_pose, 'b')
        #plt.title("gt")
        
        
        #plt.figure(3)
        #self.slam_raw.visu(plt, nb_of_pose)
        #plt.title("slam raw")
        #plt.figure(4)
        #self.gt_raw.visu(plt, nb_of_pose)
        #plt.title("gtraw")
        plt.show(block)
        #plt.show()
        
    def visuDisplacement(self, block = False):
        print(str(len(self.displacement_vec)) + " and " + str(len(self.slam.posetime)))
        plt.figure(3)
        pose_x = list()
        pose_y = list()
        size1 = list()
        for x in range(self.nb_node_backward, len(self.slam.posetime) - self.nb_node_forward):
            pose_x.append(self.slam.posetime[x][0].getPosition().x)
            pose_y.append(self.displacement_vec[x])
            size1.append(500)
        plt.scatter(pose_x, pose_y, size1, 'r')	
        plt.title("displacement")
        plt.show(block)
        

    def finalDistanceToGT(self):
        last_pose_slam = self.slam.posetime[len(self.slam.posetime) - 1][0]
        last_pose_gt = self.gt.posetime[len(self.gt.posetime) - 1][0]
        self.distance_to_gt = last_pose_gt.getPosition().dist( last_pose_slam.getPosition() )
        self.mean_distance_gt, self.mean_distance_gt_sd = self.meanAndStd(self.distance_slam_gt)

    def compute_distance_to_gt(self):
        assert len(self.slam.posetime) == len(self.gt.posetime)
        for x in range(len(self.slam.posetime)):
            pose_slam = self.slam.posetime[x][0]
            pose_gt = self.gt.posetime[x][0]
            dist = pose_gt.getPosition().dist( pose_slam.getPosition() )
            self.distance_slam_gt.append(dist)

    def meanAndStd(self, list_in):
        mean_displacement = 0
        for dis in list_in:
            mean_displacement = mean_displacement + dis
        mean_displacement = mean_displacement / len(list_in)
        
        std_deviation = 0
        xminmean = 0
        for dis in list_in:
            xminmean = xminmean + ( (dis - mean_displacement) * (dis - mean_displacement) )
        xminmean = xminmean / len(list_in)
        std_deviation = math.sqrt(xminmean)
        return (mean_displacement, std_deviation)
        
        
    def meanDisplacement(self):
        self.mean_displacement, self.std_deviation = self.meanAndStd(self.displacement_vec)
        self.mean_displacement_abs, self.std_deviation_abs = self.meanAndStd(self.displacement_vec_abs)
        assert self.mean_displacement_abs >= 0
        

    #Protected functions

    def sort(self, delta = 0):
        self.slam.posetime = []
        self.gt.posetime = []
        
        seen = list()
        seen_slam = list() # to avoid double value when rounding the time in the result file
        
        for element in self.slam_raw.posetime:
            #print("new element " + element[0].print() + " time " + str(element[1]))
            seen_slam_time = any(slam_time == element[1] for slam_time in seen_slam)
            #for slam_times in seen_slam:
                #if (element[1] == slam_times):
                    #seen_slam_time = True
            if seen_slam_time == False:
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
        


    def computeDisplacementNode(self, i_slam, i_gt, squared = True):
        """
        Compute the displacement between two nodes i_slam and i_gt
        """
        displacement = 0
        displacement_abs = 0
        node_forward_slam = i_slam + 1
        node_forward_gt = i_gt + 1
        slamposition_init = self.slam.getPose(i_slam).getPosition()
        nb_relative_relation = 0
        #print("Nb node forward")
        #print(self.nb_node_forward)
        #print("Nb node backward")
        #print(self.nb_node_backward)
        
        #print("UP")
        while node_forward_slam - i_slam <= self.nb_node_forward and node_forward_slam < len(self.slam.posetime):
            #Trans displacement 
            transdist_slam = self.slam.getTransDisplacement(i_slam, node_forward_slam)
            transdist_gt = self.gt.getTransDisplacement(i_gt, node_forward_gt)
            
            assert transdist_slam >= 0
            assert transdist_gt >= 0
            
            transnoise = 0
            if squared == True :
                transnoise = (transdist_gt - transdist_slam) * (transdist_gt - transdist_slam)
            else :
                transnoise = transdist_gt - transdist_slam
            #transnoise = abs(transnoise)
            
            #print("trans displacements ", transdist_slam, " ", transdist_gt, "trans noise ", transnoise )
            
            if self.use_translation == True:
                #print("t")
                displacement = displacement + transnoise
                displacement_abs = displacement_abs + abs(transnoise)
            
            #Rot displacement
            oriendist_slam = self.slam.getOrientationDisplacement(i_slam, node_forward_slam)
            oriendist_gt = self.gt.getOrientationDisplacement(i_gt, node_forward_gt)
            #print("orientation displacements ", oriendist_slam, " ", oriendist_gt)
            orientnoise = 0
            if squared == True :
                #print("squared")
                orientnoise = (oriendist_slam - oriendist_gt) * (oriendist_slam - oriendist_gt)
            else :
                orientnoise = oriendist_slam - oriendist_gt
            
            if self.use_orientation == True:
                #print("o")
                displacement = displacement + orientnoise
                displacement_abs = displacement_abs + abs(orientnoise)
            
            node_forward_gt = node_forward_gt + 1
            node_forward_slam = node_forward_slam + 1
            nb_relative_relation = nb_relative_relation + 1
        
        #print("DOWN")
        node_backward_slam = i_slam - 1 
        node_backward_gt = i_gt - 1
        
        while i_slam - node_backward_slam  <= self.nb_node_backward and node_backward_slam >= 0:
            #Trans displacement 
            transdist_slam = self.slam.getTransDisplacement(i_slam, node_backward_slam)
            transdist_gt = self.gt.getTransDisplacement(i_gt, node_backward_gt)
            transnoise = 0
            if squared == True :
                transnoise = (transdist_gt - transdist_slam) * (transdist_gt - transdist_slam)
            else :
                transnoise = transdist_gt - transdist_slam
            #transnoise = abs(transnoise)
            #print("trans noise " + str(transnoise))
            
            if self.use_translation == True:
                #print("t")
                displacement = displacement + transnoise
                displacement_abs = displacement_abs + abs(transnoise)
            
            #Rot displacement
            oriendist_slam = self.slam.getOrientationDisplacement(i_slam, node_backward_slam)
            oriendist_gt = self.gt.getOrientationDisplacement(i_gt, node_backward_gt)
            if squared == True :
                #print("squared")
                orientnoise = (oriendist_slam - oriendist_gt) * (oriendist_slam - oriendist_gt)
            else :
                orientnoise = oriendist_slam - oriendist_gt
            
            if self.use_orientation == True:
                #print("o")
                displacement = displacement + orientnoise
                displacement_abs = displacement_abs + abs(orientnoise)

            node_backward_gt = node_backward_gt - 1
            node_backward_slam = node_backward_slam - 1
            
            nb_relative_relation = nb_relative_relation + 1
        
        #print(nb_relative_relation)
        
        if nb_relative_relation != 0:
            return (displacement/nb_relative_relation, displacement_abs/nb_relative_relation)
        ## If nothing was calculated i.e. nb_relative_relation is 0, we return 0
        return (0, 0)
