#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Docker registry variables
REGISTRY_USER="jamesari"
REGISTRY="registry.gitlab.com"
WEB_IMAGE="$REGISTRY/$REGISTRY_USER/aswi-testing/web-dist:latest"
AI_IMAGE="$REGISTRY/$REGISTRY_USER/aswi-testing/ai-dist:latest"
DOC_IMAGE="$REGISTRY/$REGISTRY_USER/aswi-testing/doc-dist:latest"

# Products
WEB_DIRECTORY="web"
AI_DIRECTORY="ai"
DOC_DIRECTORY="web/doc/TSP"

registry_login() {
	echo "[+] Logging in..."
	echo "${ASWI_GITLAB_TOKEN}" | docker login "$REGISTRY" -u "$REGISTRY_USER" --password-stdin || { 
		echo "[-] Docker login failed"; exit 1; 
	}
}

# Builds image from the directory
# $1 - directory
# $2 - image name
build_image() {
	local directory=$1
	local image_name=$2
	
	cd "$directory" || { echo "[-] Failed to change directory to $directory"; exit 1; }
	
	echo "[>] Building image ${image_name}"

	### Multi-platform builds tbd, currently not supported for docker driver ###

	if [ "$ARCH" = "arm64" ]; then
		# ARM build
		echo "[.] Building for linux/arm64"
		docker build --platform linux/arm64 -t "$image_name" . || { echo "[-] Docker build failed for $image_name"; exit 1; }
	else
		# AMD build - default
		echo "[.] Building for linux/amd64"
		docker build --platform linux/amd64 -t "$image_name" . || { echo "[-] Docker build failed for $image_name"; exit 1; }
	fi

	echo "[<] Building image ${image_name} finished successfully"
	
	cd ..
}

# Pushes image to the registry
# $1 - image name
push_image() {
	local image_name=$1
	
	echo "[>] Publishing image ${image_name}"
	docker push "$image_name" || { echo "[-] Docker push failed for $image_name"; exit 1; }
	echo "[<] Publishing image ${image_name} finished successfully"
}

build_ai() {
	build_image "$AI_DIRECTORY" "$AI_IMAGE"
}

build_web() {
	build_image "$WEB_DIRECTORY" "$WEB_IMAGE"
}

build_doc() {
	build_image "$DOC_DIRECTORY" "$DOC_IMAGE"
}

build_and_publish_web() {
	build_web
	push_image "$WEB_IMAGE"
}

build_and_publish_ai() {
	build_ai
	push_image "$AI_IMAGE"
}

build_and_publish_doc() {
	build_doc
	push_image "$DOC_IMAGE"
}

parse_args() {
	while [[ $# -gt 0 ]]; do
		case "$1" in
			'--help'|'-h'|'help')
				print_help
				exit 0
				;;
			'--product'|'-p')
				PRODUCT="$2"
				if [ "$PRODUCT" != "web" ] && [ "$PRODUCT" != "ai" ] && [ "$PRODUCT" != "doc" ]; then
					if [ -z "$PRODUCT" ]; then
						echo "Product option requires an argument"

					else
						echo "Invalid product option: ${PRODUCT}"
					fi
					print_help
					exit 1
				fi
				shift 2
				;;
			'--build-only'|'-b')
				BUILD_ONLY=true
				shift 1
				;;
			'--arch'|'-a')
				ARCH="$2"
				if [ "$ARCH" != "amd64" ] && [ "$ARCH" != "arm64" ]; then
					if [ -z "$ARCH" ]; then
						echo "Arch option requires an argument"
					else
						echo "Invalid arch option: ${ARCH}"
					fi
					print_help
					exit 1
				fi
				shift 2
				;;
			*)
				echo "Invalid option: ${1}"
				print_help
				exit 1
				;;
		esac
	done
}

print_help() {
	echo "Usage: ${0} [OPTIONS]"
	echo "Options:"
	echo "	--product, -p <product>		Select specific product to work with (web, ai)"
	echo "	--build-only, -b		Perform build only and do not publish the image"
	echo "	--arch, -a <arch>		Select architecture to build for (amd64, arm64)"
}


run() {
	parse_args "$@"

	if [[ -n "$BUILD_ONLY" ]] && [ "$BUILD_ONLY" = true ]; then
		echo "[*] Initiating build only"
		if [ "$PRODUCT" = "web" ]; then
			build_web
		elif [ "$PRODUCT" = "ai" ]; then
			build_ai
		elif [ "$PRODUCT" = "doc" ]; then
			build_doc
		else
			build_web
			build_ai
			build_doc
		fi
	else
		echo "[*] Initiating build and publish"
		registry_login
		if [ "$PRODUCT" = "web" ]; then
			build_and_publish_web
		elif [ "$PRODUCT" = "ai" ]; then
			build_and_publish_ai
		elif [ "$PRODUCT" = "doc" ]; then
			build_and_publish_doc
		else
			build_and_publish_web
			build_and_publish_ai
			build_and_publish_doc
		fi
	fi
}

run "$@"

