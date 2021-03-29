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

## BDS GEO
* BD2-G1 C01
* BD2-G4 C04
* BD2-G5 C05
* BD2-G6 C02
* BD2-G7 C03
* BD2-G8 C18
* BD3-G1 C59
* BD3-G2 C60
* BD3-G3 C61

## TODO
* [x] RINEX2 parser
* [x] GPS satellite coordinate compute
* [x] RINEX3 parser
* [ ] BDS satellite coordinate compute
* [ ] Precision ephemeris interpolation
