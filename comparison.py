#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp

def main():
    # parse command line options
    d = kslamcomp.KSlamComp(1, 0)
    d.readSLAM("data_files/log_fuser_graph_offline_mpr.txt")
    d.readGT("data_files/log_fuser_graph_offline_laser.txt")
    print("Raw\n")
    d.printraw()
    #d.visu()
    
    ret = d.sort(0.5)
    assert(ret == True)
    print("Sorted\n")
    d.print()
    
    #d.visu()
    
    
    print("Displacement\n")
    
    displacement = d.computeDisplacementNode(1,1)
    print(displacement)
    print("\n\n")
    
    d.print()
    
    for x in range(0, d.getSLAMsize()):
        displacement_full = d.compute(x)
        print("Full displacement at step " + str(x))
        print(displacement_full)
        #d.visu(x)
        #input("Press Enter to continue...")
    
    #d.visu()
     

if __name__ == "__main__":
    main()