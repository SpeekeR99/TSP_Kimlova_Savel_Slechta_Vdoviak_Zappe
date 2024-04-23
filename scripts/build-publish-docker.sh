#!/bin/sh

# $1 is the name of the image (PACKAGE_NAME)
IMG_NAME="$CI_REGISTRY_IMAGE/$1:latest"

echo "$CI_REGISTRY_PASSWORD" | docker login $CI_REGISTRY -u $CI_REGISTRY_USER --password-stdin
cd web
docker build -t $IMG_NAME .
docker push $IMG_NAME
