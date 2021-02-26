#!/bin/sh

set -e

# 1st arg- case number (leading zero required if < 10), defaults to case1

if [ -z "${1}" ]
then
      CASE="01"
else
      CASE="${1}"
fi



echo "Downloading DICOMs"
curl  https://github.com/MavenCode/KubeflowTraining/raw/feature/ctscan-pipeline/Data/Covid-Data/dicom-covid.zip -O -J -L

echo "downloaded file..."
ls -l

unzip dicom-covid.zip -d /data/dicom-covid

#rm -d /data/dicom-covid/__MACOSX 2> /dev/null


ls -l -d /data/dicom-covid




