#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import gnuplot_reducer

def main():
	d = gnuplot_reducer.GnuplotReducer("test_files/displacement_pointcloud_position_2017-08-29-15-30-59.dat", "test_files/displacement_gmapping_laser_position_2017-08-29-15-30-59.dat")
	
	#d.print()
	
	d.reduce(1)
	d.printReducedSLAM()
	
	
if __name__ == "__main__":
    main()