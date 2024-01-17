#!/bin/bash

# MinIO 服务器信息
MINIO_ALIAS="myminio"
MINIO_SERVER_URL="http://10.8.6.30:9000"
MINIO_ACCESS_KEY="EvuKSqV607cX3C1HC7DV"
MINIO_SECRET_KEY="5D8KtKcWReCj0QrEo0tVFgstbiLm55D0uLBBcZYK"

# 配置 MinIO 客户端
./mc alias set $MINIO_ALIAS $MINIO_SERVER_URL $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

function create_user {
  local new_user=$1
  local new_password=$2

  # 创建新用户
  ./mc admin user add $MINIO_ALIAS $new_user $new_password

  if [ $? -ne 0 ]; then
    echo "创建用户失败: $new_user"
    return 1
  fi

  # 创建新桶
  ./mc mb $MINIO_ALIAS/$new_user

  if [ $? -ne 0 ]; then
    echo "创建桶失败: $new_user"
    return 1
  fi

  # 创建并应用策略
  POLICY_NAME="${new_user}_policy"
  POLICY_JSON='{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:*"
        ],
        "Resource": ["arn:aws:s3:::'$new_user'"]
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:*"
        ],
        "Resource": ["arn:aws:s3:::'$new_user'/*"]
      }
    ]
  }'

  echo "$POLICY_JSON" > policy.json

  ./mc admin policy create $MINIO_ALIAS $POLICY_NAME policy.json

  rm policy.json

  if [ $? -ne 0 ]; then
    echo "添加策略失败: $POLICY_NAME"
    return 1
  fi

  ./mc admin policy attach $MINIO_ALIAS $POLICY_NAME -u $new_user

  if [ $? -ne 0 ]; then
    echo "应用策略失败: $POLICY_NAME 到用户 $new_user"
    return 1
  fi

  echo "用户 $new_user 和桶 $new_user 已创建并配置策略"

}

users=(
  test
  test1
)

for NEW_USER in "${users[@]}"; do
  create_user $NEW_USER hanglok@8888
done
