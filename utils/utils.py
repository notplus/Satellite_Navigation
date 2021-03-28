'''
Description: 
Author: notplus
Date: 2021-03-28 21:58:33
LastEditors: notplus
LastEditTime: 2021-03-28 22:02:30
FilePath: /satellite_coordinate/utils/utils.py
'''

def parseDouble(str):
    str = str.replace('D', 'e')

    if not str.isspace():
        return float(str)
    else:
        return 0
