# coding: utf-8

def logT(s, thisL = 0, echoL = 0, mpi = False): # from py_rdee
    import time

    if echoL < thisL:
        return

    if mpi:
        from mpi4py import MPI
        print("{} - {}, rank = {}".format(time.strftime("%Y/%m/%d %H:%M:%S"), s, MPI.COMM_WORLD.Get_rank()))
    else:
        print("{} - {}".format(time.strftime("%Y/%m/%d %H:%M:%S"), s))


#**********************************************************************
# This function is used to calculate the number of days for given month
# supported format : yyyymm
#**********************************************************************
def get_ndays_of_ym(ym): # from py_rdee
    import datetime, sys
    dh_py = datetime.datetime.strptime(ym, "%Y%m")
    delta = datetime.timedelta(days = 1)
    count = 0
    while True:
        if dh_py.day == 1 and count > 0:
            break
        dh_py += delta
        count += 1

    return count



#**********************************************************************
# This function is used to render time series 
# with format of "%Y%m"
#**********************************************************************
def render_ym_series(ym1, ym2): # from py_rdee
    import datetime
    from dateutil.relativedelta import relativedelta  # datetime.timedelta doesn't support "months=1"
    ym_format = "%Y%m"
    ym1_py = datetime.datetime.strptime(ym1, ym_format)
    ym2_py = datetime.datetime.strptime(ym2, ym_format)
    delta = relativedelta(months=1)
    res = []
    while ym1_py <= ym2_py:
        res.append(ym1_py.strftime(ym_format))
        ym1_py += delta

    return res



#**********************************************************************
# This function is used to render time series 
# with format of "%Y%m%d%H"
#**********************************************************************
def render_dh_series(dh1, dh2):
    import datetime, sys
    dh_format = "%Y%m%d%H"
    dh1_py = datetime.datetime.strptime(dh1, dh_format)
    dh2_py = datetime.datetime.strptime(dh2, dh_format)
    delta = datetime.timedelta(hours = 1)
    res = []
    while dh1_py <= dh2_py:
        res.append(dh1_py.strftime(dh_format))
        dh1_py += delta

    return res



#**********************************************************************
# this function is a "map" of function np.argwhere
#**********************************************************************
def ind_eq_map(arrP, arrC, **kwargs):
    import numpy as np
    import sys

    allowMissing = False
    allowRepeat = False
    autoSort = True
    if 'allowMissing' in kwargs:
        allowMissing = kwargs['allowMissing']
    if 'allowRepeat' in kwargs:
        allowRepeat = kwargs['allowRepeat']
    if 'autoSort' in kwargs:
        autoSort = kwargs['autoSort']

    arrP_np = np.array(arrP)


    res = []
    for e in arrC:
        poss = np.argwhere(arrP_np == e).reshape(-1)
        if poss.size == 0:
            if not allowMissing:
                print(f"Error in function<ind_eq_map> cannot find value {e}!")
                sys.exit(1)
        elif poss.size > 1:
            if allowRepeat:
                res.extend(poss)  # it's ok for a list extending an nd-array
            else:
                print(f"Error in function<ind_eq_map> : value {e} repeats! set allowRepeat if it is ok!")
                sys.exit(1)
        else:
            res.extend(poss)

    if autoSort:
        res.sort()

    return res


#**********************************************************************
# this function is used to get indexes for intersection from 2 arrays
#**********************************************************************
def getIntersectInd(arr1, arr2):
    import numpy as np
    arrI = np.intersect1d(arr1, arr2)
    return ind_eq_map(arr1, arrI), ind_eq_map(arr2, arrI)

