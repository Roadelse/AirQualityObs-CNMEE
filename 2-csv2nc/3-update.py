# coding: utf-8

import numpy as np
import pandas as pd
# import xarray as xr
import netCDF4 as nc4
import re
import os.path as osp
import glob
import sys
import time
import importlib
sys.path.append('../lib')
import meelib




def update_1f(csvfile):
    # csvfile = "../../data/csvfiles/china_sites_20180408.csv"

    csvf_bname = osp.basename(csvfile)

    if 'sites' in csvf_bname:
        mode = "S" # sites
        var_suffix = ""
    elif 'cities' in csvf_bname:
        mode = 'C' # city
        var_suffix = '_city'
    else:
        print("Error! unknown csvfile!")
        sys.exit(1)

    meelib.logT(f"processing {csvf_bname}", 2, echoLevel, useMPI)

    ym = re.findall(r"20..\d\d", csvf_bname)[0]

    # xrf = xr.open_dataset(f'ncdata/CNMEE.aps.sites.{ym}.nc')

    try:
        df = pd.read_csv(csvfile)
        _ = df.iloc[0].date  # debug check
    except:
        print(f"Warning! Invalid csvfile {csvf_bname}, bytes = {osp.getsize(csvfile)}, skip")
        return
    ncf = nc4.Dataset(f'ncdata/CNMEE.aqo.site-city.{ym}.nc', 'a')

    dupCols = np.argwhere(['.1' in s for s in df.columns]).reshape(-1)
    if dupCols.size > 0:  # if dupCols (empty ndarray) will trigger Deprecated Warning 
        df.drop(df.columns[dupCols], axis = 1, inplace = True)
    css_csv = df.columns.values[3:]  # cities / sites 


    if mode == 'S':
        sites = ncf.variables['site'][:]
        sites_indHash = {s:i for i,s in enumerate(sites)}

        tarInds = [sites_indHash[s] for s in css_csv]
    else:
        cities = ncf.variables['city'][:]
        cities_indHash = {s:i for i,s in enumerate(cities)}
        # print(cities_indHash)
        tarInds = [cities_indHash[s] for s in css_csv]

    ymdhs = ncf.variables['ymdh'][:]
    for i in range(len(df)):
        rowT = df.iloc[i]
        ymdhT = f'{rowT.date}{rowT.hour:02d}'
        # print(f"procesisng row {i}, datetime : {ymdhT}")
        ind1 = np.argwhere(ymdhs == ymdhT).reshape(-1)[0]
        
        var = rowT.type
        dataT = rowT[3:].values.astype(np.float64)
        ncf.variables[f'{var}{var_suffix}'][ind1, tarInds] = dataT

    ncf.close()


def update_1m(ym):
    assert re.match(r'^20\d\d\d\d$', f'{ym}') != None, f'invalid parameter ym : {ym}'
    meelib.logT(f"processing {ym}", 1, echoLevel, useMPI)
    # csvfiles = glob.glob(dataDir + f"/china_sites_{ym}*csv")  # for test
    csvfiles = glob.glob(dataDir + f"/china*_{ym}*csv")
    for i, csvf in enumerate(csvfiles):
        update_1f(csvf)
        # if i == 5:
        #     break
    

if __name__ == '__main__':

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>> key ctrl variables
    dataDir = "../../data/csvfiles"
    start_YYYYMM = "201405"
    end_YYYYMM = "201512"

    echoLevel = 1 # print control

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>> run
    # ============= check mpi
    useMPI = False
    if importlib.util.find_spec('mpi4py'):
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size() 
        if size > 1:
            useMPI = True

    # ============= render yms
    yms = meelib.render_ym_series(start_YYYYMM, end_YYYYMM)

    # ============= run it
    if useMPI:
        print(f"Using MPI to update data, processors = {size}, rank = {rank}")
        for i in range(rank, len(yms), size):
            update_1m(yms[i])
    else:
        for ym in yms:
            update_1m(ym)

