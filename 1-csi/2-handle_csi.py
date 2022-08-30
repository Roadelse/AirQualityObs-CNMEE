# coding: utf-8

import numpy as np
import pandas as pd
import time
import geopandas as gpd
from shapely.geometry import Point


gdf = gpd.read_file(r'chinaMap\chinaCity2021.shp', encoding='cp936')

def findNearest(p):  # map obs cite to city-prov; first within, or nearest (due to sth outside)
    minD = 1e30
    minJ = -1
    for j in range(gdf.shape[0]):
        d = p.distance(gdf.geometry[j])
        if d == 0:
            lineTar = gdf.iloc[j]
            return (lineTar.city, lineTar.prov)
        else:
            if d < minD:
                minJ = j
                minD = d
    lineTar = gdf.iloc[minJ]
    return (lineTar.city, lineTar.prov)
    
def compInfo(l1, l2):       # check if the site info changes, return mark, threatening level
    if l1[1] != l2[1]:
        return 1, 0
    if l2[2] == 999 and l1[2] != 999:
        return 0, 1
    if l2[2] != 999 and l1[2] == 999:
        return 1, 1
    bias = max(abs(l1[2] - l2[2]), abs(l1[3] - l2[3]))

    if bias == 0:
        return 0, 0
    elif bias > 0.1 :
        return 4, 11
    else:
        bias_p2 = int(bias * 100) % 10
        return 3, 0 if bias_p2 == 0 else bias_p2 + 1
    
    #   return 0, 0


df = pd.read_csv('csi_all.csv')
vLen = df['监测点编码'].unique().size # valid len


df2 = pd.DataFrame(columns = ['code', 'name', 'city', 'prov', 'nation', 'lat', 'lon', 'risk'])


df2.nation = ['中国' for _ in range(vLen)]


kcMap = {}
k = 0
codeVaryCount = 0
for i in range(len(df)):
    code, name, lat, lon = df.loc[i, '监测点编码'], df.loc[i, '监测点名称'], df.loc[i, '纬度'], df.loc[i, '经度']
    risk = 0
    k2 = k
    if code in kcMap:  # update code info
        compRes, risk = compInfo(df2.loc[kcMap[code], ['code', 'name', 'lat', 'lon']].to_list(),  [code, name, lat, lon])
        if compRes == 0 :
            continue
        else:
            if compRes == 4:
                print(df2.loc[kcMap[code], ['code', 'name', 'lat', 'lon']].to_list(), [code, name, lat, lon])
            codeVaryCount += 1
            k2 = kcMap[code]
    
    
    df2.loc[k2, ['code', 'name', 'lat', 'lon']] = code, name, lat, lon

    df2.loc[k2, 'risk'] = max(risk, df2.loc[k2, 'risk'])
    
    kcMap[code] = k2
    try:
        if lat != 999 :
            df2.loc[k2, ['city', 'prov']] = findNearest(Point(lon, lat))
        else:
            df2.loc[k2, 'city'] = df.loc[i, '城市']
    except:
        print(i, k)
        raise
    
    if k2 == k : # update code info
        k += 1  
        # print(f"k = {k}, code = {code}")


df2.to_csv("csi.csv", index=False)
