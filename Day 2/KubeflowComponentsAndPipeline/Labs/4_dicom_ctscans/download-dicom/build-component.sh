#!/bin/sh

image_name=mavencodev/download-dicom # Specify the image name here
image_tag=1.0.12-charles
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build -t "${full_image_name}" .
docker push "$full_image_name"
