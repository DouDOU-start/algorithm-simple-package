if [ $ALGORITHM_NAME ];
then
	read -e -p "请输入安装算法名称: " -i "${ALGORITHM_NAME}" ALGORITHM_NAME
else
	read -e -p "请输入安装算法名称: " -i "lungsegmentation" ALGORITHM_NAME
fi

if [ $ALGORITHM_VERSION ];
then
	read -e -p "请输入安装算法版本: " -i "${ALGORITHM_VERSION}" ALGORITHM_VERSION
else
	read -e -p "请输入安装算法版本: " -i "0.1.3" ALGORITHM_VERSION
fi

docker run --gpus 1 --name test hanglok/${ALGORITHM_NAME}:${ALGORITHM_VERSION} agent.py sst.nii.gz "http://192.168.5.164:9000/algorithm/input/test1.nii.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=afK2BE5BSWvayIw546b2%2F20231206%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231206T030231Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=4d30f08185a83776633d1b200617e3a5eeae140666c84dc2cd2f9ae5140442fc"

docker run --gpus 1 --name test \
-e FILE_NAME="sst.nii.gz" \
-e URL="http://192.168.5.164:9000/algorithm/input/851d6332-801d-4690-98d4-6fbb8f84615c.nii.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=afK2BE5BSWvayIw546b2%2F20231206%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231206T103312Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=e9226181540d4cdc405bcb6f02479cf132d247d39f227e51aa392bc46298d798" \
hanglok/airwaysegmentation:0.1.3 \
python agent.py