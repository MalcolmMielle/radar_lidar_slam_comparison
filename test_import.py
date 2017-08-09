#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp
from kslamcomp import kslamcomp_logger

def main():
    # parse command line options
    d = kslamcomp.KSlamComp(1, 0)
    d.read("data_files/shifted.txt")
    print("Raw\n")
    d.printraw()
    
    d.sort()
    print("Sorted\n")
    d.print()
    
    
    print("Displacement\n")
    
    displacement = d.computeDisplacementNode(1,1)
    print(displacement)
    print("\n\n")
    
    displacement_full = d.compute()
    print("Full displacement")
    print(displacement_full)
    
    d.visu()
    
    
    d_logger = kslamcomp_logger.KSlamComp_logger("slam.gpl", 1, 0)
    d_logger.read("data_files/shifted.txt")
    d_logger.sort()
    displacement_full = d_logger.compute()
     

if __name__ == "__main__":
    main()
