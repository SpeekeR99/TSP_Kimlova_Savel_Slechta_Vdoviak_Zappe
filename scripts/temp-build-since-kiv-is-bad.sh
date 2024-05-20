#!/bin/sh

REGISTRY_USER="jamesari"
REGISTRY="registry.gitlab.com"
WEB_IMG_NAME="$REGISTRY/$REGISTRY_USER/aswi-testing/web-dist:latest"
AI_IMG_NAME="$REGISTRY/$REGISTRY_USER/aswi-testing/ai-dist:latest"

echo "$ASWI_GITLAB_TOKEN" | docker login $REGISTRY -u $REGISTRY_USER --password-stdin

build_and_push_image() {
	local directory=$1
	local image_name=$2
	
	cd "$directory"
	
	echo "Building image: $image_name"
	docker build -t "$image_name" .
	docker build --platform linux/amd64 -t "$image_name" .
	
	echo "Pushing image: $image_name"
	docker push "$image_name"
	
	cd ..
}

if [ "$1" = "web" ]; then
	build_and_push_image "web" "$WEB_IMG_NAME"
elif [ "$1" = "ai" ]; then
	build_and_push_image "ai" "$AI_IMG_NAME"
else
	build_and_push_image "web" "$WEB_IMG_NAME"
	build_and_push_image "ai" "$AI_IMG_NAME"
fi