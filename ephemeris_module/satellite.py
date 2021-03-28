'''
Description: 
Author: notplus
Date: 2021-03-28 17:04:31
LastEditors: notplus
LastEditTime: 2021-03-28 19:59:13
FilePath: /satellite_coordinate/ephemeris_module/satellite.py
'''
from abc import ABC, abstractmethod

class Satellite(ABC):

    @abstractmethod
    def ComputeCoord(self, t):
        pass
