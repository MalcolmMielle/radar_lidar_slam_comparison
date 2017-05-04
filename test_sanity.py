#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import data
from kslamcomp import kslamcomp

def main():
    # parse command line options
    d = kslamcomp.KSlamComp(1, 0)
    d.read("data_files/shifted.txt")
    d.printraw()
    d.sort()
    d.print()
    
    d_invert = kslamcomp.KSlamComp(0, 1)
    d_invert.read("data_files/shifted.txt")
    d_invert.printraw()
    d_invert.sort()
    d_invert.print()
    
    #d.printraw()
    
    displacement = d.computeDisplacementNode(0,0)
    displacement_inv = d_invert.computeDisplacementNode(1,1)
    assert displacement == displacement_inv
    
    displacement_full = d.compute()
    displacement_full_inv = d_invert.compute()
    assert displacement_full == displacement_full_inv
     

if __name__ == "__main__":
    main()