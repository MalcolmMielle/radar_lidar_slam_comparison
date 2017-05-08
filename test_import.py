#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp

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
     

if __name__ == "__main__":
    main()