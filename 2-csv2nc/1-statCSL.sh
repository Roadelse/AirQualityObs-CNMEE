#!/bin/bash

# This script is used to stat City/Site List for each month
# by zjx @2022-08 in zjlab-11B-303


outDir=CS-Lists 		# output directory

mkdir -p $outDir


ymS=201405  	# start YYYYMM
ymE=202207  	# end YYYYMM

ym=$ymS

while [[ $ym -le $ymE ]]
do
	echo `date +%Y/%m/%d-%H:%M:%S`' : processing '$ym
	# ----------- handle Site first
	head -n 1  ../../data/csvfiles/china_sites_${ym}* | grep -Po '\d\d\d\dA' | sort | uniq > $outDir/sites.${ym}.txt

	# ----------- handle City Next
	cfiles=(../../data/csvfiles/china_cities_${ym}*)
	for cf in "${cfiles[@]}"
	do
		head "$cf" -n 1 | cut -d, -f4- >> .cbd
	done
	sed -i 's/,/\n/g' .cbd
	sort .cbd | uniq > $outDir/cities.${ym}.txt
	rm .cbd

	# ----------- loop next YYYYMM
	ym=`date -d "${ym}01 +1 month"  +%Y%m`
done