#!/bin/bash

read -e -p "请输入 Minio地址: " -i "http://10.8.6.30:9000" MINIO_URL
read -e -p "请输入 Minio用户名: " -i "" USER_NAME
read -e -s -p "请输入 Minio密码: " -i "" PASSWORD
echo ""

# 配置 MinIO 客户端
MC_ALIAS="myminio"
./mc alias set $MC_ALIAS $MINIO_URL $USER_NAME $PASSWORD

read -e -p "请选择本地文件或路径: " -i "" LOCAL_PATH
read -e -p "请选择上传到 Minio的路径: " -i "" REMOTE_PATH

# 检查 LOCAL_PATH 是文件还是目录
if [ -d "$LOCAL_PATH" ]; then
    # 如果是目录，使用 --recursive 标志
    ./mc cp --recursive ${LOCAL_PATH} "${MC_ALIAS}/${USER_NAME}/${REMOTE_PATH}"
elif [ -f "$LOCAL_PATH" ]; then
    # 如果是文件，正常复制
    ./mc cp ${LOCAL_PATH} "${MC_ALIAS}/${USER_NAME}/${REMOTE_PATH}"
else
    echo "指定的本地路径不存在或不是一个有效的文件/目录。"
fi