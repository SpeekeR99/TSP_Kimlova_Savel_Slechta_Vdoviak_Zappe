#!/bin/sh

# $1 is the name of the image (PACKAGE_NAME)
IMG_NAME="$CI_REGISTRY_IMAGE/$1:latest"

cd web
ls -la
docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
docker build -t $IMG_NAME .
docker push $IMG_NAME
