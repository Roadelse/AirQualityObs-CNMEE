#!/bin/bash


# Must deprecated "站点列表-旧-946个.csv"

files=(`ls ../../data/_站点列表/*csv`)

outFile=csi_all.csv

# [[ -e $outFile ]] && rm -f $outFile

echo '监测点编码,监测点名称,城市,经度,纬度,' > $outFile
for f in ${files[@]}
do
	sed -n '2,$p' $f >> $outFile
done


# --- handle bad data

# replace - with ""
sed -i 's/-//g' $outFile

# replace "" with 999

sed -i 's/,,/,999,999/' $outFile
# sed -i 's/,,,/,999,999,/' $outFile
