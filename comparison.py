#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp
from kslamcomp import gnuplot_reducer

import math

distance_to_gt = dict()


def to_latex_table(file_name, summary_table_file):
    
    round_up = lambda num : math.ceil(num * 1000) / 1000
    
    
    f = open(file_name, 'w')
    
    #f.write(r"\begin{table*}[t]" + "\n" + r"\centering" + "\n" + r"\begin{tabular}{m{1.6cm}cccccccccccc}" + "\n" +r"\toprule" + "\n" + r"& \multicolumn{4}{c}{First run} & \multicolumn{4}{c}{Second Run} & \multicolumn{4}{c}{Third Run} \\" + "\n" + r"\cmidrule(lr){2-5}\cmidrule(lr){6-9}\cmidrule(lr){10-13}" + "\n" + r"& \multicolumn{2}{c}{NDT Fuser} & \multicolumn{2}{c}{Gmapping} & \multicolumn{2}{c}{NDT Fuser} & \multicolumn{2}{c}{Gmapping} & \multicolumn{2}{c}{NDT Fuser} & \multicolumn{2}{c}{Gmapping} \\" + "\n" + r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}\cmidrule(lr){10-11}\cmidrule(lr){12-13}" + "\n" + r"& Radar & Velodyne & Radar & Velodyne & Radar & Velodyne & Radar & Velodyne & Radar & Velodyne & Radar & Velodyne \\ \midrule")
   
    f.write("Distance to ground truth" +\
        " & "+ str( distance_to_gt['d_first_fuser_radar'] ) + \
        " & "+ str( distance_to_gt['d_first_fuser_velodyne'] ) + \
        " & "+ str( distance_to_gt['d_first_gmapping_radar'] ) + \
        " & "+ str( distance_to_gt['d_first_gmapping_velodyne'] ) +\
        " & "+ str( distance_to_gt['d_second_fuser_radar'] ) + \
        " & "+ str( distance_to_gt['d_second_fuser_velodyne'] ) +\
        " & "+ str( distance_to_gt['d_second_gmapping_radar'] ) + \
        " & "+ str( distance_to_gt['d_second_gmapping_velodyne'] ) +\
        " & "+ str( distance_to_gt['d_third_fuser_radar'] ) +\
        " & "+ str( distance_to_gt['d_third_fuser_velodyne'] ) +\
        " & "+ str( distance_to_gt['d_third_gmapping_radar'] ) +\
        " & "+ str( distance_to_gt['d_third_gmapping_velodyne'] ) + r"\\")


    mean_distance_to_gt_radar_fuser = round_up( ( distance_to_gt['d_first_fuser_radar'] + distance_to_gt['d_second_fuser_radar'] + distance_to_gt['d_third_fuser_radar'] ) / 3 )
    mean_distance_to_gt_radar_gmapping = round_up( ( distance_to_gt['d_first_gmapping_radar'] + distance_to_gt['d_second_gmapping_radar'] + distance_to_gt['d_third_gmapping_radar'] ) / 3 )
    mean_distance_to_gt_velodyne_fuser = round_up( ( distance_to_gt['d_first_fuser_velodyne'] + distance_to_gt['d_second_fuser_velodyne'] + distance_to_gt['d_third_fuser_velodyne'] ) / 3 )
    mean_distance_to_gt_velodyne_gmapping = round_up( ( distance_to_gt['d_first_gmapping_velodyne'] + distance_to_gt['d_second_gmapping_velodyne'] + distance_to_gt['d_third_gmapping_velodyne'] ) / 3 )

    f.write("\n\n")

    f.write("Mean displacement in position & \makecell{"+ str( distance_to_gt['dp_first_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_first_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dp_first_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_first_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dp_first_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_first_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dp_first_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_first_gmapping_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dp_second_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_second_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dp_second_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_second_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dp_second_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_second_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dp_second_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_second_gmapping_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dp_third_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_third_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dp_third_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_third_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dp_third_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_third_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dp_third_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dpsd_third_gmapping_velodyne'] ) + r"}\\")
    
    mean_position_displacement_radar_fuser = round_up( ( distance_to_gt['dp_first_fuser_radar'] + distance_to_gt['dp_second_fuser_radar'] + distance_to_gt['dp_third_fuser_radar'] ) / 3 )
    mean_position_displacement_radar_gmapping = round_up( ( distance_to_gt['dp_first_gmapping_radar'] + distance_to_gt['dp_second_gmapping_radar'] + distance_to_gt['dp_third_gmapping_radar'] ) / 3 )
    mean_position_displacement_velodyne_fuser = round_up( ( distance_to_gt['dp_first_fuser_velodyne'] + distance_to_gt['dp_second_fuser_velodyne'] + distance_to_gt['dp_third_fuser_velodyne'] ) / 3 )
    mean_position_displacement_velodyne_gmapping = round_up( ( distance_to_gt['dp_first_gmapping_velodyne'] + distance_to_gt['dp_second_gmapping_velodyne'] + distance_to_gt['dp_third_gmapping_velodyne'] ) / 3 )
    

    f.write("\n\n")

    f.write("Mean displacement in orientation & \makecell{"+ str( distance_to_gt['do_first_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_first_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['do_first_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_first_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['do_first_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_first_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['do_first_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_first_gmapping_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['do_second_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_second_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['do_second_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_second_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['do_second_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_second_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['do_second_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_second_gmapping_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['do_third_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_third_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['do_third_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_third_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['do_third_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_third_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['do_third_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dosd_third_gmapping_velodyne'] ) + r"}\\")
    
    mean_orientation_displacement_radar_fuser = round_up( ( distance_to_gt['do_first_fuser_radar'] + distance_to_gt['do_second_fuser_radar'] + distance_to_gt['do_third_fuser_radar'] ) / 3 )
    mean_orientation_displacement_radar_gmapping = round_up( ( distance_to_gt['do_first_gmapping_radar'] + distance_to_gt['do_second_gmapping_radar'] + distance_to_gt['do_third_gmapping_radar'] ) / 3 )
    mean_orientation_displacement_velodyne_fuser = round_up( ( distance_to_gt['do_first_fuser_velodyne'] + distance_to_gt['do_second_fuser_velodyne'] + distance_to_gt['do_third_fuser_velodyne'] ) / 3 )
    mean_orientation_displacement_velodyne_gmapping = round_up( ( distance_to_gt['do_first_gmapping_velodyne'] + distance_to_gt['do_second_gmapping_velodyne'] + distance_to_gt['do_third_gmapping_velodyne'] ) / 3 )


    f.write("\n\n")

    f.write("Mean distance to gt & \makecell{"+ str( distance_to_gt['dgt_first_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_first_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_first_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_first_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_first_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_first_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_first_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_first_gmapping_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_second_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_second_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_second_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_second_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_second_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_second_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_second_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_second_gmapping_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_third_fuser_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_third_fuser_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_third_fuser_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_third_fuser_velodyne'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_third_gmapping_radar'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_third_gmapping_radar'] ) + "} & \makecell{"+ str( distance_to_gt['dgt_third_gmapping_velodyne'] ) + r"\\$\pm$"+ str( distance_to_gt['dgtsd_third_gmapping_velodyne'] ) + r"}\\")

    f.close()
    
    
    f_summary = open(summary_table_file, 'w')
    
    
    #f_summary.write("Mean distance to gt & " + str(mean_distance_to_gt_radar_fuser) + " & " + str(mean_distance_to_gt_velodyne_fuser) + " & " + str(mean_distance_to_gt_radar_gmapping) + " & " + str(mean_distance_to_gt_velodyne_gmapping) + r"\\")
    #f_summary.write("\n\n")
    f_summary.write("Mean displacement in position & " + str(mean_position_displacement_radar_fuser) + " & " + str(mean_position_displacement_velodyne_fuser) + " & " + str(mean_position_displacement_radar_gmapping) + " & " + str(mean_position_displacement_velodyne_gmapping) + r"\\")
    f_summary.write("\n\n")
    f_summary.write("Mean displacement in orientation & " + str(mean_orientation_displacement_radar_fuser) + " & " + str(mean_orientation_displacement_velodyne_fuser) + " & " + str(mean_orientation_displacement_radar_gmapping) + " & " + str(mean_orientation_displacement_velodyne_gmapping) + r"\\")
    
    f_summary.close()
    
    
    #Distance to ground truth                & 3.57  & 0.35 & 0.98 & 0.35 & 0.60 & 0.18 & 1.21 & 0.34 & 0.26 & 0.06 & 0.07 & 0.07 \\
    
    #Mean displacement in position           & 
    #\makecell{0.06 \\$\pm$ 0.19} & \makecell{0.005 \\$\pm$ 0.005} & \makecell{0.01 \\$\pm$ 0.03} & \makecell{0.01 \\$\pm$ 0.03} &
    #\makecell{0.035 \\$\pm$ 0.06} & \makecell{0.015 \\$\pm$ 0.02} & \makecell{0.01 \\$\pm$ 0.02} & \makecell{0.01 \\$\pm$ 0.02} &
    #\makecell{0.03 \\$\pm$ 0.03} & \makecell{0.01 \\$\pm$ 0.01} & \makecell{0.01 \\$\pm$ 0.035} & \makecell{0.01 \\$\pm$ 0.03} \\
    
    #Accumulated displacement in orientation & 
    #\makecell{0.03 \\$\pm$ 0.04} & \makecell{0.001 \\$\pm$ 0.001} & \makecell{0.004 \\$\pm$ 0.01} & \makecell{0.001 \\$\pm$ 0.001} &
    #\makecell{0.02 \\$\pm$ 0.02} & \makecell{0.003 \\$\pm$ 0.004} & \makecell{0.004 \\$\pm$ 0.01} & \makecell{0.001 \\$\pm$ 0.001} &
    #\makecell{0.02 \\$\pm$ 0.02} & \makecell{0.002 \\$\pm$ 0.003} & \makecell{0.0045 \\$\pm$ 0.01} & \makecell{0.001 \\$\pm$ 0.001} \\

def reduce_files_gmapping(gmapping_files, use_position):
    for el in gmapping_files:
        reducer = gnuplot_reducer.GnuplotReducer(el.gt, el.file_name)
        #d.print()
        kslam = reducer.reduce(2)
        kslam.use_translation = use_position
        kslam.use_orientation = not use_position
        ret = kslam.sort(0.5)
        assert(ret == True)
        print("Sorted")
        
        if el.min_distance == 1:
            ##print("TRIM")
            kslam.trim_odometry(0.009)

        kslam.compute(-1, False)

        kslam.meanDisplacement()
        kslam.finalDistanceToGT()

        #if use_position:
        kslam.exportGnuplot(el.file_out_position)
        #else:
        #kslam.exportGnuplot(el.file_out_orientation)

        kslam.add_to_dictionnary(el.file_out_orientation, distance_to_gt)


class Pair:
    def __init__(self, file_name, gt_name, file_out_position, file_out_orientation, min_d = -1, is_rad = True, cov_rad = False):
        self.file_name = file_name
        self.gt = gt_name
        self.file_out_position = file_out_position
        self.file_out_orientation = file_out_orientation
        self.is_radian = is_rad
        self.convert_to_rad = cov_rad
        self.min_distance = min_d

def main():
    
    min_dist = 1
    
    names = list()
    ####NDT laserscan
    names.append(Pair("data_files/log_fuser_pointcloud_offline_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "results/displacement_fuser_pointcloud_position_offline_people_long.dat", "results/displacement_fuser_pointcloud_orientation_offline_people_long.dat"))
    names.append(Pair("data_files/log_fuser_pointcloud_offline_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-30-59.dat"))
    names.append(Pair("data_files/log_fuser_pointcloud_offline_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-37-08.dat"))

    ####NDT mpr
    names.append(Pair("data_files/log_fuser_mpr_offline_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "results/displacement_fuser_mpr_position_offline_people_long.dat", "results/displacement_fuser_mpr_orientation_offline_people_long.dat"))
    names.append(Pair("data_files/log_fuser_mpr_offline_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat"))
    names.append(Pair("data_files/log_fuser_mpr_offline_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat"))

    ###Gmapping laser scan
    names.append(Pair("data_files/GMapping/gmapping_laser_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "results/displacement_gmapping_laser_position_people_long.dat", "results/displacement_gmapping_laser_orientation_people_long.dat", min_dist, False, True))
    names.append(Pair("data_files/GMapping/gmapping_laser_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_gmapping_laser_position_2017-08-29-15-30-59.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-30-59.dat", min_dist, False, True))
    names.append(Pair("data_files/GMapping/gmapping_laser_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_gmapping_laser_position_2017-08-29-15-37-08.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-37-08.dat", min_dist, False, True))

    ###Gmapping mpr
    names.append(Pair("data_files/GMapping/gmapping_mpr_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "results/displacement_gmapping_mpr_position_people_long.dat", "results/displacement_gmapping_mpr_orientation_people_long.dat", min_dist, False, True))
    names.append(Pair("data_files/GMapping/gmapping_mpr_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_gmapping_mpr_position_2017-08-29-15-30-59.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-30-59.dat", min_dist, False, True))
    names.append(Pair("data_files/GMapping/gmapping_mpr_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_gmapping_mpr_position_2017-08-29-15-37-08.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-37-08.dat", min_dist, False, True))

    #for i in range(2):
        #use_position = True
        #if i == 1:
            #use_position = False
            
        #for el in names:
            ## parse command line options
            #d = kslamcomp.KSlamComp(1, 0)
            #d.use_translation = use_position
            #d.use_orientation = not use_position
            ##d.readSLAM("data_files/log_fuser_pointcloud_offline_people_long.txt")
            ##d.readSLAM("data_files/log_fuser_mpr_offline_2017-08-29-15-30-59.txt")
            #d.readSLAM(el.file_name, -1, el.is_radian, el.convert_to_rad)
            #d.readGT(el.gt)
            
            
            ##d.readGT("data_files/log_fuser_vmc_2017-08-29-15-30-59.txt")
            ##d.readGT("data_files/log_fuser_vmc_2017-08-29-15-37-08.txt")
            #print("Read")
            ##d.printraw()
            ##d.visu()
            
            #ret = d.sort(0.5)
            #assert(ret == True)
            #print("Sorted")
            ##d.print()
            ##if el.min_distance == 1:
                ###print("TRIM")
                ##d.trim_odometry(0.009)
            
            ##d.visu()
            
            
            #print("Displacement")
            
            ##displacement = d.computeDisplacementNode(1,1)
            ##print(displacement)
            ##print("\n\n")
            
            ##d.print()
            #if use_position:
                #d.compute(-1, False)
            #else:
                #d.compute(-1, False)
            
            ##for x in range(0, d.getSLAMsize()):
                ##displacement_full = d.compute(x, False)
                ##print("Full displacement at step " + str(x))
                ##print(displacement_full)
                ###d.visu(x)
                ###input("Press Enter to continue...")
            
            ##d.visu()
            ##d.printDisplacement()
            ##d.visuDisplacement()
            
            #d.meanDisplacement()
            #d.finalDistanceToGT()
            
            #if use_position:
                #d.exportGnuplot(el.file_out_position)
            #else:
                #d.exportGnuplot(el.file_out_orientation)
    
    #Reduce values of gmapping now
    
    gmapping_files = list()
    gmapping_files_orientations = list()

    ######People_long - all against mpr times for meaningful comparison
    ##Gmapping laser position 
    gmapping_files.append(Pair("results/displacement_gmapping_laser_position_people_long.dat", "results/displacement_fuser_mpr_position_offline_people_long.dat", "results/displacement_gmapping_laser_position_people_long_smaller.dat", "third_gmapping_velodyne", min_dist))
    ##Gmapping mpr position
    gmapping_files.append(Pair("results/displacement_gmapping_mpr_position_people_long.dat", "results/displacement_fuser_mpr_position_offline_people_long.dat", "results/displacement_gmapping_mpr_position_people_long_smaller.dat", "third_gmapping_radar", min_dist))
    ##Gmapping laser orientation
    gmapping_files_orientations.append(Pair("results/displacement_gmapping_laser_orientation_people_long.dat", "results/displacement_fuser_mpr_orientation_offline_people_long.dat", "results/displacement_gmapping_laser_orientation_people_long_smaller.dat", "third_gmapping_velodyne", min_dist))
    ##Gmapping mpr orientation
    gmapping_files_orientations.append(Pair("results/displacement_gmapping_mpr_orientation_people_long.dat", "results/displacement_fuser_mpr_orientation_offline_people_long.dat", "results/displacement_gmapping_mpr_orientation_people_long_smaller.dat", "third_gmapping_radar", min_dist))

    ## Same with NDT fuser
    ##Fuser laser position 
    gmapping_files.append(Pair("results/displacement_fuser_pointcloud_position_offline_people_long.dat", "results/displacement_fuser_mpr_position_offline_people_long.dat", "results/displacement_fuser_pointcloud_position_offline_people_long_smaller.dat", "third_fuser_velodyne"))
    ##Fuser mpr position NOT Needed DONE FOR THE EXPORT OF LATEX
    gmapping_files.append(Pair("results/displacement_fuser_mpr_position_offline_people_long.dat", "results/displacement_fuser_mpr_position_offline_people_long.dat", "results/displacement_fuser_mpr_position_offline_people_long_smaller.dat", "third_fuser_radar"))
    ##Fuser laser orientation
    gmapping_files_orientations.append(Pair("results/displacement_fuser_pointcloud_orientation_offline_people_long.dat", "results/displacement_fuser_mpr_orientation_offline_people_long.dat", "results/displacement_fuser_pointcloud_orientation_offline_people_long_smaller.dat", "third_fuser_velodyne"))
    ##Fuser mpr orientation NOT NEEDED
    gmapping_files_orientations.append(Pair("results/displacement_fuser_mpr_orientation_offline_people_long.dat", "results/displacement_fuser_mpr_orientation_offline_people_long.dat", "results/displacement_fuser_mpr_orientation_offline_people_long_smaller.dat", "third_fuser_radar"))

    ######30-59 - all against mpr times for meaningful comparison
    ##Gmapping laser position 
    gmapping_files.append(Pair("results/displacement_gmapping_laser_position_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_laser_position_2017-08-29-15-30-59_smaller.dat", "first_gmapping_velodyne", min_dist))
    ##Gmapping mpr position
    gmapping_files.append(Pair("results/displacement_gmapping_mpr_position_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_mpr_position_2017-08-29-15-30-59_smaller.dat", "first_gmapping_radar", min_dist))
    ##Gmapping laser orientation
    gmapping_files_orientations.append(Pair("results/displacement_gmapping_laser_orientation_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-30-59_smaller.dat", "first_gmapping_velodyne", min_dist))
    ##Gmapping mpr orientation
    gmapping_files_orientations.append(Pair("results/displacement_gmapping_mpr_orientation_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-30-59_smaller.dat", "first_gmapping_radar", min_dist))

    ## Same with NDT fuser
    ##Fuser laser position 
    gmapping_files.append(Pair("results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-30-59_smaller.dat", "first_fuser_velodyne"))
    ##Fuser mpr position NOT Needed
    gmapping_files.append(Pair("results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59_smaller.dat", "first_fuser_radar"))
    ##Fuser laser orientation
    gmapping_files_orientations.append(Pair("results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-30-59_smaller.dat", "first_fuser_velodyne"))
    ##Fuser mpr orientation NOT NEEDED
    gmapping_files_orientations.append(Pair("results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59_smaller.dat", "first_fuser_radar"))


    ######37-08 - all against mpr times for meaningful comparison
    ##Gmapping laser position 
    gmapping_files.append(Pair("results/displacement_gmapping_laser_position_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_laser_position_2017-08-29-15-37-08_smaller.dat", "second_gmapping_velodyne", min_dist))

    gmapping_files.append(Pair("results/displacement_gmapping_mpr_position_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_mpr_position_2017-08-29-15-37-08_smaller.dat", "second_gmapping_radar", min_dist))
    gmapping_files_orientations.append(Pair("results/displacement_gmapping_laser_orientation_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-37-08_smaller.dat", "second_gmapping_velodyne", min_dist))
    gmapping_files_orientations.append(Pair("results/displacement_gmapping_mpr_orientation_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-37-08_smaller.dat", "second_gmapping_radar", min_dist))


    ## Same with NDT fuser
    ##Fuser laser position 
    gmapping_files.append(Pair("results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-37-08_smaller.dat", "second_fuser_velodyne"))
    ##Fuser mpr position NOT Needed
    gmapping_files.append(Pair("results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08_smaller.dat", "second_fuser_radar"))
    ##Fuser laser orientation
    gmapping_files_orientations.append(Pair("results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-37-08_smaller.dat", "second_fuser_velodyne"))
    ##Fuser mpr orientation NOT NEEDED
    gmapping_files_orientations.append(Pair("results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08_smaller.dat", "second_fuser_radar"))

    ##TODO LAST NDT

    assert len(gmapping_files_orientations) == 12
    assert len(gmapping_files) == 12

    reduce_files_gmapping(gmapping_files, True)
    reduce_files_gmapping(gmapping_files_orientations, False)

    to_latex_table("results/table_all_results.tex", "results/table_means.tex")
     

if __name__ == "__main__":
    main()
