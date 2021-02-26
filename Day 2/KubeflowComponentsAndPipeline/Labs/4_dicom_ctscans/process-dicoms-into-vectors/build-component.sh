#!/usr/bin/env bash

image_name=mavencodev/covid-prep-dicom # Specify the image name here
image_tag=1.0.2-charles
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build -t "${full_image_name}" .
docker push "$full_image_name"
