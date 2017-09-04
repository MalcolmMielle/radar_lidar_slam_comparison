#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp

def main():
    # parse command line options
    d = kslamcomp.KSlamComp(1, 0)
    #d.readSLAM("data_files/log_fuser_pointcloud_offline_people_long.txt")
    #d.readSLAM("data_files/log_fuser_mpr_offline_2017-08-29-15-30-59.txt")
    d.readSLAM("data_files/log_fuser_mpr_offline_2017-08-29-15-37-08.txt")
    #d.readGT("data_files/log_fuser_vmc_people_long.txt")
    #d.readGT("data_files/log_fuser_vmc_2017-08-29-15-30-59.txt")
    d.readGT("data_files/log_fuser_vmc_2017-08-29-15-37-08.txt")
    print("Raw\n")
    d.printraw()
    #d.visu()
    
    ret = d.sort(0.5)
    assert(ret == True)
    print("Sorted\n")
    d.print()
    
    d.visu()
    
    
    print("Displacement\n")
    
    displacement = d.computeDisplacementNode(1,1)
    print(displacement)
    print("\n\n")
    
    d.print()
    
    for x in range(0, d.getSLAMsize()):
        displacement_full = d.compute(x, False)
        print("Full displacement at step " + str(x))
        print(displacement_full)
        #d.visu(x)
        #input("Press Enter to continue...")
    
    #d.visu()
    d.printDisplacement()
    d.visuDisplacement()
    
    d.exportGnuplot("displacement.dat")
     

if __name__ == "__main__":
    main()
