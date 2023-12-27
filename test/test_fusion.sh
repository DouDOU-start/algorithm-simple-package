#!/bin/bash

exec_env=$(jq -r '.fusion' exec_env.json)
minio_env=$(jq -r '.minio_env' exec_env.json)

# echo $exec_env
# echo $minio_env

docker run --rm --shm-size=1g \
-e EXEC_ENV="$exec_env" \
-e MINIO_ENV="$minio_env" \
hanglok/fusion:0.0.1