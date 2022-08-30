# coding: utf-8

import xarray as xr
import numpy as np
import os
import pandas as pd
import sys
sys.path.append('../lib')
import meelib

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> pre-defined informations
varList = ["AQI", "PM2.5", "PM2.5_24h", "PM10", "PM10_24h", "SO2", "SO2_24h", "NO2", "NO2_24h", "O3", "O3_24h", "O3_8h", "O3_8h_24h", "CO", "CO_24h"]
units = ['ug/m3' for _ in varList]
units[0] = ''
units[-1] = 'mg/m3'
units[-2] = 'mg/m3'


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> key ctrl variables
start_YYYYMM, end_YYYYMM = '201405', '202207'
outDir = "ncdata"
csi_file = '../1-csi/csi.csv'

echoLevel = 1  # print control

# ================= dependent
yms = meelib.render_ym_series(start_YYYYMM, end_YYYYMM)
os.makedirs(outDir, exist_ok = True)


df_csi = pd.read_csv(csi_file)
df_csi.set_index(['code'], inplace = True)



def init_1m(ym):

    with open(f'CS-Lists/sites.{ym}.txt') as f:
        siteCodes = f.read().splitlines()
    with open(f'CS-Lists/cities.{ym}.txt', encoding = "utf-8") as f:
        cityNames = f.read().splitlines()

    ym_days = meelib.get_ndays_of_ym(ym)
    ymdhs = meelib.render_dh_series(f"{ym}0100", f"{ym}{ym_days}23")

    arrS = np.full((len(ymdhs), len(siteCodes)), np.nan)
    arrC= np.full((len(ymdhs), len(cityNames)), np.nan)

    ds = xr.Dataset()

    ds.coords['site'] = ("site", siteCodes)
    ds.coords['city'] = ('city', cityNames)
    ds.coords['ymdh'] = ("ymdh", ymdhs)



    ds['site_name'] = ("site", df_csi.loc[siteCodes, :].name.values)
    ds['site_city'] = ("site", df_csi.loc[siteCodes, :].city.values)
    ds['site_prov'] = ("site", df_csi.loc[siteCodes, :].prov.values)
    ds['site_nation'] = ("site", df_csi.loc[siteCodes, :].nation.values)
    ds['site_lat'] = ("site", df_csi.loc[siteCodes, :].lat.values)
    ds['site_lon'] = ("site", df_csi.loc[siteCodes, :].lon.values)
    ds['site_risk'] = ("site", df_csi.loc[siteCodes, :].risk.values)

    for i, v in enumerate(varList):
        ds[v] = (("ymdh", "site"), arrS)
        if units[i]:
            ds[v].attrs['units'] = units[i]
    for i, v in enumerate(varList):
        ds[f"{v}_city"] = (("ymdh", "city"), arrC)
        if units[i]:
            ds[f"{v}_city"].attrs['units'] = units[i]

    ds.attrs['source'] = 'https://quotsoft.net/air/'

    # encoding = {v : {"_FillValue" : None, "zlib" : True, "complevel" : 1} for v in varList}
    encoding = {v : {"_FillValue" : None, 'dtype' : 'float32'} for v in varList}
    encoding.update({f'{v}_city' : {"_FillValue" : None, 'dtype' : 'float32'} for v in varList})



    ds.to_netcdf(f'ncdata/CNMEE.aqo.site-city.{ym}.nc', encoding=encoding, format='netCDF4')


for ym in yms:
    meelib.logT(f"processing {ym}", 1, echoLevel)
    init_1m(ym)
    # break
