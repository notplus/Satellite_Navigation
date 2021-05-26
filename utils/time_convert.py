'''
Description: 
Author: notplus
Date: 2021-03-22 09:33:09
LastEditors: notplus
LastEditTime: 2021-04-21 19:56:45
'''

import datetime


class Time(datetime.datetime):
    def __new__(cls, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        cls.__float_second = second+microsecond/1e6
        return datetime.datetime.__new__(cls, year, month, day, hour, minute,
                                         second, microsecond, tzinfo=tzinfo,  fold=fold)

    def UTC(self):
        return self.utctimetuple()

    def GPST(self):
        return self.isoweekday() % 7 * 3600*24+self.hour*3600+self.minute*60+self.get_float_second()

    def BDST(self):
        return self.GPST()-14

    def get_float_second(self):
        return self.__float_second

    def set_float_second(self, float_sec):
        self.__float_second = float_sec
    
    def clone(self):
        t = Time(self.year,self.month,self.day,self.hour,self.minute,self.second)
        t.set_float_second(self.get_float_second())
        return t
