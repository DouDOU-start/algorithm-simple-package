#!/bin/bash

cleanup() {
    # 清理垃圾文件
    rm -rf algorithm
    rm -rf rootfs
}

# 设置 trap
trap cleanup EXIT

build_tip="
===================================================================================================
===================================================================================================
#                                                                                                 #
#                                                                                                 #
#                               欢迎使用算法打包服务                                              #
#                                                                                                 #
#                                                                                                 #
===================================================================================================
===================================================================================================
"
echo -e "${YELLOW}${build_tip}${POS}${BLACK}"

echo "Author: \"Allen_Huang\""
echo "Email: \"1021217094@qq.com\""
echo ""

if [ $ALGORITHM_DIR ];
then
	read -e -p "请输入算法目录名称: " -i "${ALGORITHM_DIR}" ALGORITHM_DIR
else
	read -e -p "请输入算法目录名称: " -i "lungsegmentation" ALGORITHM_DIR
fi

# 使用配置文件 config.ini 来替代交互式版本确认
# if [ $CUDA_VERSION ];
# then
# 	read -e -p "请输入Cuda版本: " -i "${CUDA_VERSION}" CUDA_VERSION
# else
# 	read -e -p "请输入Cuda版本: " -i "11.8.0" CUDA_VERSION
# fi

# if [ $PYTHON_VERSION ];
# then
# 	read -e -p "请输入Python版本: " -i "${PYTHON_VERSION}" PYTHON_VERSION
# else
# 	read -e -p "请输入Python版本: " -i "3.9.10" PYTHON_VERSION
# fi

start=$(date +%s)

rm -rf algorithm

if [ "$ALGORITHM_DIR" = "fusion" ]; then
    cp -rf $ALGORITHM_DIR algorithm
else
    cp -rf ../$ALGORITHM_DIR algorithm
fi

cp -rf agent.py algorithm

if [ -d "algorithm/rootfs" ]; then
    mv algorithm/rootfs .
fi

if [ ! -d "rootfs" ]; then
	mkdir -p "rootfs"
fi

ALGORITHM_NAME=$(grep '^name =' algorithm/config.ini | cut -d '=' -f2 | tr -d ' \r')
ALGORITHM_VERSION=$(grep '^version =' algorithm/config.ini | cut -d '=' -f2 | tr -d ' \r')
PYTHON_VERSION=$(grep '^python =' algorithm/config.ini | cut -d '=' -f2 | tr -d ' \r')
CUDA_VERSION=$(grep '^cuda =' algorithm/config.ini | cut -d '=' -f2 | tr -d ' \r')

BASE_VERSION="cuda_$CUDA_VERSION-python_$PYTHON_VERSION"

docker build --no-cache -t 10.8.6.34:5000/algorithm/${ALGORITHM_NAME,,}:${ALGORITHM_VERSION} . \
--ulimit nofile=1024000:1024000 \
--build-arg BASE_VERSION=$BASE_VERSION \
--build-arg NEXUS_IP=10.8.6.60

end=$(date +%s)
runtime=$((end-start))

echo "打包成功！执行时长: $runtime s"