#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kslamcomp import kslamcomp


class KSlamComp_logger(kslamcomp.KSlamComp):
        """
        Compute like normal but output a gnuplot friendly log file of the displacement
        """
        def __init__(self, file_out, forward_nodes_lookup = 1, backward_nodes_lookup = 0, slam_input_raw = None, gt_input_raw = None):
                kslamcomp.KSlamComp.__init__(self, forward_nodes_lookup, backward_nodes_lookup, slam_input_raw, gt_input_raw)
                self.file_out = file_out
                f = open(self.file_out, 'w')
                f.write("# pose_nb, displacement\n\n")
                f.close()


        def compute(self, nb_of_pose = -1):
                """
                Compute the total error in the SLAM. Don't forget to call sort before
                """

                displacement = 0
                #print(len(self.slam.posetime))
                if nb_of_pose > len(self.slam.posetime) or nb_of_pose < 0:
                        nb_of_pose = len(self.slam.posetime)
                for x in range(0, nb_of_pose):
                        displacement = displacement + self.computeDisplacementNode(x, x)
                        f = open(self.file_out, 'a')
                        str_out = str(x)+" "+str(displacement)+"\n"
                        f.write(str_out)
                        f.close()
                return displacement
