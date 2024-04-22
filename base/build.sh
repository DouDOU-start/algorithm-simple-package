#!/bin/bash

if [ $CUDA_VERSION ];
then
	read -e -p "请输入Cuda版本: " -i "${CUDA_VERSION}" CUDA_VERSION
else
	read -e -p "请输入Cuda版本: " -i "11.8.0" CUDA_VERSION
fi

if [ $PYTHON_VERSION ];
then
	read -e -p "请输入Python版本: " -i "${PYTHON_VERSION}" PYTHON_VERSION
else
	read -e -p "请输入Python版本: " -i "3.9.10" PYTHON_VERSION
fi

VERSION="cuda_$CUDA_VERSION-python_$PYTHON_VERSION"
IMAGE_NAME="algorithm-base"

# 加速构建镜像 --ulimit nofile=1024000:1024000
docker build -t 10.8.6.34:5000/hanglok/${IMAGE_NAME}:${VERSION} . \
--ulimit nofile=1024000:1024000 \
--build-arg CUDA_VERSION=$CUDA_VERSION \
--build-arg PYTHON_VERSION=$PYTHON_VERSION