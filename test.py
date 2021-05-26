'''
Description: 
Author: notplus
Date: 2021-04-21 16:09:48
LastEditors: notplus
LastEditTime: 2021-05-26 08:30:49
FilePath: /satellite_coordinate/test.py
'''
from utils.time_convert import Time
from positioning.single_point import SinglePointPositioning

import unittest
import numpy as np

class TestSPP(unittest.TestCase):
    def test_chan_3100(self):
        spp = SinglePointPositioning(
            "demo/ephemeris_data/brdc3100.20n", "../obs/obs/chan3100.20o")
        ax, ay, az = -0.267442768572702E+07, 0.375714305701559E+07, 0.439152148514515E+07
        error = np.zeros([10,3])
        for i in range(10):
            x, y, z = spp.positioning(Time(2020, 11, 5,i*2))
            error[i,:]=np.array([abs(x-ax),abs(y-ay),abs(z-az)])
        print("--------------------")
        print("chan mean error:")
        print("X:%f"%np.mean(error,axis=0)[0])
        print("Y:%f"%np.mean(error,axis=0)[1])
        print("Z:%f"%np.mean(error,axis=0)[2])
        print("chan max/min error:")
        print("X:%f/%f"%(np.max(error,axis=0)[0],np.min(error,axis=0)[0]))
        print("Y:%f/%f"%(np.max(error,axis=0)[1],np.min(error,axis=0)[1]))
        print("Z:%f/%f"%(np.max(error,axis=0)[2],np.min(error,axis=0)[2]))

        self.assertLess(np.mean(error,axis=0)[0],10,msg="X direction error is too large")
        self.assertLess(np.mean(error,axis=0)[1],10,msg="Y direction error is too large")
        self.assertLess(np.mean(error,axis=0)[2],10,msg="Z direction error is too large")

        
    def test_leij_3100(self):
        spp = SinglePointPositioning(
            "demo/ephemeris_data/brdc3100.20n", "../obs/obs/leij3100.20o")
        ax, ay, az = 0.389873613453103E+07,0.855345521080705E+06,0.495837257579542E+07
        error = np.zeros([10,3])
        for i in range(10):
            x, y, z = spp.positioning(Time(2020, 11, 5,i*2))
            error[i,:]=np.array([abs(x-ax),abs(y-ay),abs(z-az)])
        print("--------------------")
        print("leij mean error:")
        print("X:%f"%np.mean(error,axis=0)[0])
        print("Y:%f"%np.mean(error,axis=0)[1])
        print("Z:%f"%np.mean(error,axis=0)[2])
        print("leij max/min error:")
        print("X:%f/%f"%(np.max(error,axis=0)[0],np.min(error,axis=0)[0]))
        print("Y:%f/%f"%(np.max(error,axis=0)[1],np.min(error,axis=0)[1]))
        print("Z:%f/%f"%(np.max(error,axis=0)[2],np.min(error,axis=0)[2]))
        self.assertLess(np.mean(error,axis=0)[0],10,msg="X direction error is too large")
        self.assertLess(np.mean(error,axis=0)[1],10,msg="Y direction error is too large")
        self.assertLess(np.mean(error,axis=0)[2],10,msg="Z direction error is too large")

    def test_warn_3100(self):
        spp = SinglePointPositioning(
            "demo/ephemeris_data/brdc3100.20n", "../obs/obs/warn3100.20o")
        ax, ay, az = 0.365878555276965E+07,0.784471127238666E+06,0.514787071062059E+07
        error = np.zeros([10,3])
        for i in range(10):
            x, y, z = spp.positioning(Time(2020, 11, 5,i*2))
            error[i,:]=np.array([abs(x-ax),abs(y-ay),abs(z-az)])
        print("--------------------")
        print("warn mean error:")
        print("X:%f"%np.mean(error,axis=0)[0])
        print("Y:%f"%np.mean(error,axis=0)[1])
        print("Z:%f"%np.mean(error,axis=0)[2])
        print("warn max/min error:")
        print("X:%f/%f"%(np.max(error,axis=0)[0],np.min(error,axis=0)[0]))
        print("Y:%f/%f"%(np.max(error,axis=0)[1],np.min(error,axis=0)[1]))
        print("Z:%f/%f"%(np.max(error,axis=0)[2],np.min(error,axis=0)[2]))
        self.assertLess(np.mean(error,axis=0)[0],10,msg="X direction error is too large")
        self.assertLess(np.mean(error,axis=0)[1],10,msg="Y direction error is too large")
        self.assertLess(np.mean(error,axis=0)[2],10,msg="Z direction error is too large")

if __name__ == '__main__':
    unittest.main()