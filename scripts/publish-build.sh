#!/bin/sh

SOURCE=$1
TARGET=$2

echo "Source: ${SOURCE}, Target: ${TARGET}"

for file in ./$SOURCE/*
do
	echo "File: ${file}"
	FILENAME="$(basename -- $file)"
	curl --fail-with-body --header "JOB-TOKEN: $CI_JOB_TOKEN" --upload-file $file "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/generic/$TARGET/rolling/${FILENAME}"
done