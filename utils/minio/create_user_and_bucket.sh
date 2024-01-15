#!/bin/bash

# MinIO 服务器信息
MINIO_ALIAS="myminio"
MINIO_SERVER_URL="http://10.8.6.30:9000"
MINIO_ACCESS_KEY="<admin-access-key>"
MINIO_SECRET_KEY="<admin-secret-key>"

# 新用户信息
NEW_USER="newusername"
NEW_PASSWORD="newpassword"

# 新桶名称
NEW_BUCKET="newbucketname"

# 配置 MinIO 客户端
mc alias set $MINIO_ALIAS $MINIO_SERVER_URL $MINIO_ACCESS_KEY $MINIO_SECRET_KEY

# 创建新用户
mc admin user add $MINIO_ALIAS $NEW_USER $NEW_PASSWORD

# 创建新桶
mc mb $MINIO_ALIAS/$NEW_BUCKET

# 创建并应用策略
POLICY_NAME="${NEW_USER}_policy"
POLICY_JSON='{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": ["arn:aws:s3:::'$NEW_BUCKET'"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListMultipartUploadParts",
        "s3:AbortMultipartUpload"
      ],
      "Resource": ["arn:aws:s3:::'$NEW_BUCKET'/*"]
    }
  ]
}'
echo $POLICY_JSON | mc admin policy add $MINIO_ALIAS $POLICY_NAME -
mc admin policy set $MINIO_ALIAS $POLICY_NAME user=$NEW_USER

echo "用户 $NEW_USER 和桶 $NEW_BUCKET 已创建并配置策略"
