#!/usr/bin/env bash

#docker login --username=mavencodev

echo 'mvn compile and package uber jar'
mvn install:install-file -Dfile=./jar/mahout-core-14.1-scala_2.11.jar -DgroupId=org.apache.mahout -DartifactId=mahout-core -Dversion=14.1 -Dpackaging=jar
mvn install:install-file -Dfile=./jar/mahout-spark-14.1-scala_2.11.jar -DgroupId=org.apache.mahout -DartifactId=mahout-spark -Dversion=14.1 -Dpackaging=jar
mvn package

echo 'docker build and package'
image_name=mavencodev/covid-basis-vectors # Specify the image name here
image_tag=1.0.0-charles
full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker build -t "${full_image_name}" .
docker push "$full_image_name"
