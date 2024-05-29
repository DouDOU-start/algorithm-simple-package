#!/bin/bash

# images=10.8.6.34:5000/algorithm/bodyinference:0.1.3
images=10.8.6.34:5000/algorithm/liverboneskinsegmentation:wfz-240102

# docker pull $images

exec_env=$(jq -r '.bodyinference' exec_env.json)
minio_env=$(jq -r '.minio_env' exec_env.json)

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
-e MINIO_ENV="$minio_env" \
$images