#!/usr/bin/env bash
set -e

# 1st arg- case number (leading zero required if < 10), defaults to case1

if [ -z "${1}" ]
then
      CASE="01"
else
      CASE="${1}"
fi



echo "Downloading DICOMs"
wget https://github.com/MavenCode/KubeflowTraining/raw/feature/ctscan-pipeline/Data/Covid-Data/dicom-covid.zip
unzip dicom-covid.zip -d /tmp/dicom-covid
mv /tmp/dicom-covid /data/dicom



