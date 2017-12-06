#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp
from kslamcomp import gnuplot_reducer

class Pair:
	def __init__(self, file_name, gt_name, file_out_position, file_out_orientation, is_rad = True):
		self.file_name = file_name
		self.gt = gt_name
		self.file_out_position = file_out_position
		self.file_out_orientation = file_out_orientation
		self.is_radian = is_rad

def main():
	names = list()
	####NDT laserscan
	####names.append(Pair("data_files/log_fuser_pointcloud_offline_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "displacement_fuser_pointcloud_offline_people_long.dat"))
	names.append(Pair("data_files/log_fuser_pointcloud_offline_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-30-59.dat"))
	names.append(Pair("data_files/log_fuser_pointcloud_offline_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-37-08.dat"))
	
	####NDT mpr
	####names.append(Pair("data_files/log_fuser_mpr_offline_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "displacement_fuser_mpr_offline_people_long.dat"))
	names.append(Pair("data_files/log_fuser_mpr_offline_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat"))
	names.append(Pair("data_files/log_fuser_mpr_offline_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat"))
	
	####Gmapping laser scan
	names.append(Pair("data_files/GMapping/gmapping_laser_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "results/displacement_gmapping_laser_position_people_long.dat", "results/displacement_gmapping_laser_orientation_people_long.dat", False))
	names.append(Pair("data_files/GMapping/gmapping_laser_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_gmapping_laser_position_2017-08-29-15-30-59.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-30-59.dat", False))
	names.append(Pair("data_files/GMapping/gmapping_laser_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_gmapping_laser_position_2017-08-29-15-37-08.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-37-08.dat", False))
	
	####Gmapping mpr
	names.append(Pair("data_files/GMapping/gmapping_mpr_people_long.txt", "data_files/log_fuser_vmc_people_long.txt", "displacement_gmapping_mpr_position_people_long.dat", "results/displacement_gmapping_mpr_orientation_people_long.dat", False))
	names.append(Pair("data_files/GMapping/gmapping_mpr_2017-08-29-15-30-59.txt", "data_files/log_fuser_vmc_2017-08-29-15-30-59.txt", "results/displacement_gmapping_mpr_position_2017-08-29-15-30-59.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-30-59.dat", False))
	names.append(Pair("data_files/GMapping/gmapping_mpr_2017-08-29-15-37-08.txt", "data_files/log_fuser_vmc_2017-08-29-15-37-08.txt", "results/displacement_gmapping_mpr_position_2017-08-29-15-37-08.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-37-08.dat", False))
	
	for i in range(2):
		use_position = True
		if i == 1:
			use_position = False
			
		for el in names:
			# parse command line options
			d = kslamcomp.KSlamComp(1, 0)
			d.use_translation = use_position
			d.use_orientation = not use_position
			#d.readSLAM("data_files/log_fuser_pointcloud_offline_people_long.txt")
			#d.readSLAM("data_files/log_fuser_mpr_offline_2017-08-29-15-30-59.txt")
			d.readSLAM(el.file_name, el.is_radian)
			d.readGT(el.gt)
			#d.readGT("data_files/log_fuser_vmc_2017-08-29-15-30-59.txt")
			#d.readGT("data_files/log_fuser_vmc_2017-08-29-15-37-08.txt")
			print("Read")
			#d.printraw()
			#d.visu()
			
			ret = d.sort(0.5)
			assert(ret == True)
			print("Sorted")
			#d.print()
			
			#d.visu()
			
			
			print("Displacement")
			
			#displacement = d.computeDisplacementNode(1,1)
			#print(displacement)
			#print("\n\n")
			
			#d.print()
			if use_position:
				d.compute(-1, True)
			else:
				d.compute(-1, False)
			
			#for x in range(0, d.getSLAMsize()):
				#displacement_full = d.compute(x, False)
				#print("Full displacement at step " + str(x))
				#print(displacement_full)
				##d.visu(x)
				##input("Press Enter to continue...")
			
			#d.visu()
			#d.printDisplacement()
			#d.visuDisplacement()
			
			if use_position:
				d.exportGnuplot(el.file_out_position)
			else:
				d.exportGnuplot(el.file_out_orientation)
     
     ##Reduce values of gmapping now
     
	gmapping_files = list()
	
	gmapping_files.append(Pair("results/displacement_gmapping_laser_position_2017-08-29-15-30-59.dat", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_laser_position_2017-08-29-15-30-59_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_laser_position_2017-08-29-15-37-08.dat", "results/displacement_fuser_pointcloud_position_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_laser_position_2017-08-29-15-37-08_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_mpr_position_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_mpr_position_2017-08-29-15-30-59_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_mpr_position_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_position_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_mpr_position_2017-08-29-15-37-08_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_laser_orientation_2017-08-29-15-30-59.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-30-59_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_laser_orientation_2017-08-29-15-37-08.dat", "results/displacement_fuser_pointcloud_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_laser_orientation_2017-08-29-15-37-08_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_mpr_orientation_2017-08-29-15-30-59.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-30-59.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-30-59_smaller.dat", ""))
	
	gmapping_files.append(Pair("results/displacement_gmapping_mpr_orientation_2017-08-29-15-37-08.dat", "results/displacement_fuser_mpr_orientation_offline_2017-08-29-15-37-08.dat", "results/displacement_gmapping_mpr_orientation_2017-08-29-15-37-08_smaller.dat", ""))
	
	for el in gmapping_files:
		d = gnuplot_reducer.GnuplotReducer(el.gt, el.file_name)
		#d.print()
		d.reduce(1)
		print("Reduced ", el.file_out_position)
		d.exportGnuplot(el.file_out_position)
     

if __name__ == "__main__":
    main()
