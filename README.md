# AirQualityObs-CNMEE
Normalization of chinese air quality observation data (published by Ministry of Ecology and Environment)

数据处理脚本, csv转netcdf, 方便后续处理

处理流程:
   1. (1-csi/) 整理sites & cities
   2. (2-csv2nc/) csv转netcdf
   3. (3-query/) 数据查询

查询功能支持 (3-query/config.py中设定):
   * 选定数据后屏幕打印