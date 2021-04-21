'''
Description: 
Author: notplus
Date: 2021-04-02 08:30:05
LastEditors: notplus
LastEditTime: 2021-04-21 09:26:37
FilePath: /satellite_coordinate/observation/observation.py
'''

import math
from utils.time_convert import Time


class _ObsRecord(object):
    def __init__(self, year, month, day, hour, minute, second):
        # self.year = year
        # self.month = month
        # self.day = day
        # self.hour = hour
        # self.minute = minute
        # self.second = second
        self.epoch = Time(year, month, day, hour, minute, int(
            second), int((second-int(second))*1e6))
        self.data = dict()

def takeEpoch(record):
    return record.epoch


class Observation(object):
    def __init__(self, path):
        self.__parseFile(path)

    def __parseFile(self, path):
        print("parse file %s" % path)
        with open(path, 'r') as f:
            lines = f.readlines()

            # RINEX 2.11 Observation
            # parse header

            i = 0

            # line 1 RINEX VERSION / TYPE
            self.__rinex_version = float(lines[i][0:9])
            self.__type = lines[i][20:21]
            i += 1

            # line 2 PGM / RUN BY / DATE
            self.__pgm = lines[i][0:20]
            self.__run_by = lines[i][20:40]
            self.__data = lines[i][40:60]
            i += 1

            # COMMENT (optional)
            # self.__comments = []
            while lines[i][60:80].strip() == "COMMENT":
                # self.__comments += [lines[i][0:60]]
                i += 1

            # MARKER NAME
            if lines[i][60:80].strip() == "MARKER NAME":
                self.__marker_name = lines[i][0:60]
                i += 1

            # MARKER NUMBER (optional)
            self.__marker_number = []
            while lines[i][60:80].strip() == "MARKER NUMBER":
                self.__marker_number += [lines[i][0:20]]
                i += 1

            # OBSERVER / AGENCY
            if lines[i][60:80].strip() == "OBSERVER / AGENCY":
                self.__observer = lines[i][0:20]
                self.__agency = lines[i][20:60]
                i += 1

            # REC # / TYPE / VERS
            if lines[i][60:80].strip() == "REC # / TYPE / VERS":
                self.__rec = lines[i][0:20]
                self.__rec_type = lines[i][20:40]
                self.__rec_vers = lines[i][40:60]
                i += 1

            # ANT # / TYPE
            if lines[i][60:80].strip() == "ANT # / TYPE":
                self.__antenna_number = lines[i][0:20]
                self.__antenna_type = lines[i][20:40]
                i += 1

            # APPROX POSITION XYZ
            if lines[i][60:80].strip() == "APPROX POSITION XYZ":
                self.__approx_x = float(lines[i][0:14])
                self.__approx_y = float(lines[i][14:28])
                self.__approx_z = float(lines[i][28:42])
                i += 1

            # ANTENNA: DELTA H/E/N
            if lines[i][60:80].strip() == "ANTENNA: DELTA H/E/N":
                self.__antenna_height = float(lines[i][0:14])
                self.__antenna_delta_e = float(lines[i][14:28])
                self.__antenna_delta_n = float(lines[i][28:42])
                i += 1

            # WAVELENGTH FACT L1/2 (optional)
            self.__wavelength = []
            while lines[i][60:80].strip() == "WAVELENGTH FACT L1/2":
                self.__wavelength += [int(lines[i][0:6])]
                self.__wavelength += [int(lines[i][6:12])]
                i += 1

            # # / TYPES OF OBSERV
            if lines[i][60:80].strip() == "# / TYPES OF OBSERV":
                self.__observation_type_num = int(lines[i][0:6])
                self.__observation_type = []

                # while lines[i][60:80].strip() == "# / TYPES OF OBSERV":
                for j in range(math.ceil(self.__observation_type_num/9)):
                    end = 9
                    if j*9+9 > self.__observation_type_num:
                        end = self.__observation_type_num-j*9
                    for ii in range(end):
                        self.__observation_type += [lines[i][10+ii*6:12+ii*6]]
                    i += 1
                # for ii in range(self.__observation_type_num%9):
                #     self.__observation_type += [lines[i][10+ii*6:12+ii*6]]
                # i+=1

            while lines[i][60:80].strip() != "END OF HEADER":
                # INTERVAL (optional)
                if lines[i][60:80].strip() == "INTERVAL":
                    self.__interval = float(lines[i][0:10])
                    i += 1

                # TIME OF FIRST OBS
                if lines[i][60:80].strip() == "TIME OF FIRST OBS":
                    self.__time_of_first_obs_year = int(lines[i][0:6])
                    self.__time_of_first_obs_month = int(lines[i][6:12])
                    self.__time_of_first_obs_day = int(lines[i][12:18])
                    self.__time_of_first_obs_hour = int(lines[i][18:24])
                    self.__time_of_first_obs_min = int(lines[i][24:30])
                    self.__time_of_first_obs_sec = float(lines[i][30:43])
                    self.__time_system = lines[48:51]

                    i += 1

                # TIME OF LAST OBS (optional)
                if lines[i][60:80].strip() == "TIME OF LAST OBS":
                    self.__time_of_last_obs_year = int(lines[i][0:6])
                    self.__time_of_last_obs_month = int(lines[i][6:12])
                    self.__time_of_last_obs_day = int(lines[i][12:18])
                    self.__time_of_last_obs_hour = int(lines[i][18:24])
                    self.__time_of_last_obs_min = int(lines[i][24:30])
                    self.__time_of_last_obs_sec = float(lines[i][30:43])
                    # self.__time_system = lines[48:51]
                    i += 1

                # RCV CLOCK OFFS APPL (optional)
                if lines[i][60:80].strip() == "RCV CLOCK OFFS APPL":
                    self.__rcv_clock_offs_appl = int(lines[i][0:6])
                    i += 1

                # LEAP SECONDS (optional)
                if lines[i][60:80].strip() == "LEAP SECONDS":
                    self.__leap_seconds = int(lines[i][0:6])
                    i += 1

                # # OF SATELLITES  (optional)
                if lines[i][60:80].strip() == "# OF SATELLITES ":
                    self.__of_satellites = int(lines[i][0:6])
                    i += 1

                # PRN / # OF OBS (optional)
                if lines[i][60:80].strip() == "PRN / # OF OBS":
                    self.__prn_of_obs_num = int(lines[i][0:6])

                    for j in range(math.ceil(self.__prn_of_obs_num/9)):
                        end = 9
                        if j*9+9 > self.__prn_of_obs_num:
                            end = self.__prn_of_obs_num-j*9
                        # for ii in range(end):

                        i += 1

                # COMMENT (optional)
                while lines[i][60:80].strip() == "COMMENT":
                    # self.__comments += [lines[i][0:60]]
                    i += 1

            # END OF HEADER
            if lines[i][60:80].strip() == "END OF HEADER":
                i += 1

            # observation records
            self.__records = []

            while i < len(lines):
                if lines[i].startswith("                            4  1"):
                    i += 2
                    continue
                obs_rec = _ObsRecord(int(lines[i][1:3])+2000, int(lines[i][4:6]), int(lines[i][7:9]),
                                     int(lines[i][10:12]), int(lines[i][13:15]), float(lines[i][15:26]))

                epoch_flag = int(lines[i][28:29])

                if epoch_flag == 0:
                    num_satellites = int(lines[i][29:32])
                    # receiver clock offset (seconds, optional) F12.9

                    for j in range(math.ceil(num_satellites/12)):
                        end = 12
                        if j*12+12 > num_satellites:
                            end = num_satellites-j*12
                        for ii in range(end):
                            obs_rec.data[lines[i][32+ii*3:35+ii*3]] = dict()
                        i += 1

                    for s in obs_rec.data.keys():
                        for ii in range(math.ceil(self.__observation_type_num/5)):
                            end = 5
                            if ii*5+5 > self.__observation_type_num:
                                end = self.__observation_type_num-ii*5
                            for j in range(end):
                                obs_type = self.__observation_type[ii*5+j]
                                obs_rec.data[s][obs_type] = dict()
                                if lines[i][j*16:14+j*16].strip() != '':
                                    obs_rec.data[s][obs_type]['Obs'] = float(
                                        lines[i][j*16:14+j*16])
                                    obs_rec.data[s][obs_type]['LLI'] = lines[i][14+j*16:15+j*16]
                                    obs_rec.data[s][obs_type]['Signal_strength'] = lines[i][15+j*16:16+j*16]
                            i += 1

                    self.__records += [obs_rec]

        self.__records.sort(key=takeEpoch)

    def find_last_observation(self, t) -> _ObsRecord:
        for i in range(1, len(self.__records)):
            if abs((t-self.__records[i-1].epoch).total_seconds()) <= abs((t-self.__records[i].epoch).total_seconds()):
                return self.__records[i-1]
