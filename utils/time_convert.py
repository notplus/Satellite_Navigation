'''
Description: 
Author: notplus
Date: 2021-03-22 09:33:09
LastEditors: notplus
LastEditTime: 2021-03-29 11:05:46
'''

import datetime


class Time(datetime.datetime):
    def __new__(cls, year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0):
        return datetime.datetime.__new__(cls, year, month, day, hour, minute,
                                         second, microsecond, tzinfo=tzinfo,  fold=fold)

    def UTC(self):
        return self.utctimetuple()

    def GPST(self):
        return self.isoweekday() % 7 * 3600*24+self.hour*3600+self.minute*60+self.second

    def BDST(self):
        return self.GPST()-14
