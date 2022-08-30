# coding=utf-8

# This script is used to query data from ../2-csv2nc/ncdata 
# only support stdout-print by now
# by zjx @2022-08-30 11:25:11 in zjlab-11B

import sys
import netCDF4 as nc4
import numpy as np
import pandas as pd
import os.path
sys.path.append('../lib')
import meelib

dataDir = "../2-csv2nc/ncdata/"

if __name__ == '__main__':
    import config

    # >>>>>>>>>>>>>>>>>>>>>>> resolve config and prepare
    mode = config.mode
    ymdhs = config.datehours
    sites = config.sites
    variables = config.variables

    yms = list(set(map(lambda x : x[:6], ymdhs)))

    dataHolder = np.full((len(ymdhs), len(sites), len(variables)), np.nan)


    # >>>>>>>>>>>>>>>>>>>>>>> get data
    for ym in yms:
        ncfT = nc4.Dataset(os.path.join(dataDir, f"CNMEE.aqo.site-city.{ym}.nc"))
        ymdhsF = ncfT.variables['ymdh'][:]
        sitesF = ncfT.variables['site'][:]

        siteIndexA, siteIndexF = meelib.getIntersectInd(sites, sitesF)
        timeIndexA, timeIndexF = meelib.getIntersectInd(ymdhs, ymdhsF)
        # print(siteIndexA, siteIndexF)
        # print(timeIndexA, timeIndexF)

        for i_v, v in enumerate(variables):
            dataHolder[np.ix_(timeIndexA, siteIndexA, [i_v])] = ncfT.variables[v][timeIndexF, siteIndexF][:, :, None]  # fuck np slice broadcasting grammar

        
    # >>>>>>>>>>>>>>>>>>>>>>> show data
    data2d = dataHolder.reshape(len(ymdhs) * len(sites), len(variables))
    df = pd.DataFrame(data2d, index = pd.MultiIndex.from_product([ymdhs, sites], names = ['ymdh', 'site']), columns = variables)

    print(df)

