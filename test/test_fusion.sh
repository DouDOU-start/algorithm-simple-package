#!/bin/bash

images=10.8.6.34:5000/algorithm/fusion:0.0.1

docker pull $images

exec_env=$(jq -r '.fusion' exec_env.json)
minio_env=$(jq -r '.minio_env' exec_env.json)

docker run --rm --shm-size=1g \
-e EXEC_ENV="$exec_env" \
-e MINIO_ENV="$minio_env" \
$images