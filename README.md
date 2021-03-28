# Satellite Coordinate Compute


## Demo Data format

brdc\*\*\*\*\.\*\*n
为IGS提供的GPS广播星历文件，文件中只包括GPS的星历数据。

brdm\*\*\*\*.\*\*p
为IGS提供的多系统广播星历文件，文件中包括GNSS四系统和部分其他系统的星历数据。

igs\*\*\*\*\*.sp3
为IGS提供的GPS精密星历文件。

gbm\*\*\*\*\*.sp3
为gbm提供的多系统精密星历文件。

## TODO
* [x] RINEX2 parser
* [x] GPS satellite coordinate compute
* [ ] RINEX3 parser
* [ ] BDS satellite coordinate compute
* [ ] Precision ephemeris interpolation
