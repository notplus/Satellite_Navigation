# Satellite Navigation

## 阶段性作业
1. 卫星坐标计算： 

   * 使用说明：`python3 compute.py -e /path/to/ephemeris_file -o /path/to/output_file`
   * 可通过`python3 compute.py -h`获取参数说明
   * 依赖`numpy`

   * demo：
      * `python3 compute.py -e ./demo/ephemeris_data/brdc3100.20n -o ./demo/result/brdc3100.txt`
      * `python3 compute.py -e ./demo/ephemeris_data/brdm3130.20p -o ./demo/result/brdm3130.txt`
   * `./demo/result/brdc3100.txt`为`brdc3100.20n`转换的精密星历
   * `./demo/result/brdm3130.txt`为`brdm3130.20p`转换的精密星历 (仅有GPS数据)
   * 输出的起止时间、卫星、间隔时间参数(分钟单位)需要在`compute.py`中48、51、52(54、55)行中调整


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
* [ ] Observation file parser
