#!/bin/bash

tarFile=csi.csv

while read line
do
	if [[ -z "$line" ]]; then continue; fi
	echo ${line}
	code=`echo $line | cut -d, -f1`
	sed -i "/$code/c $line" $tarFile

done < citeInfo_search.csv

# sed -i "/3019A/d" $tarFile
