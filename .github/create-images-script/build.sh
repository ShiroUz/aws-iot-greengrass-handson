#!/bin/bash
set -eu
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

DOCKERFILE_DIR="${GITHUB_WORKSPACE}/docker"
DOCKER_IMAGE_NAME=packer-raspberrypi-imager

DOCKER_BUILDKIT=1 docker build -t ${DOCKER_IMAGE_NAME} ${DOCKERFILE_DIR}

# Create directories if they don't exist
mkdir -p ${GITHUB_WORKSPACE}/packer_cache
mkdir -p ${GITHUB_WORKSPACE}/output-arm-image

ls -l ${GITHUB_WORKSPACE}
ls -l ${PWD}

docker run \
  --rm \
  --privileged \
  -v ${GITHUB_WORKSPACE}:/build:ro \
  -v ${GITHUB_WORKSPACE}/packer_cache:/build/packer_cache \
  -v ${GITHUB_WORKSPACE}/output-arm-image:/build/output-arm-image \
  ${DOCKER_IMAGE_NAME} build /build/.github/create-images-script/packer_raspberrypi.json