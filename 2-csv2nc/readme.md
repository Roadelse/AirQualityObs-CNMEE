# readme

处理csv格式的空气质量观测数据, 包括所有站点和城市, 逐月以netcdf格式存储

处理流程:

   1. 1-statCLS.sh : 获取每个月的站点列表和城市列表, 存储于./CS-lists

   2. 2-init.py : 初始化每个月的nc文件, 先以nan填充

   3. 3-update.py : 根据csv数据文件更新nc数据, 支持mpi并行运行 (
    e.g., mpiexec -n 4 python 3-update.py)

