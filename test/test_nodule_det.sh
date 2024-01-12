#!/bin/bash

# mc_client="$1"

# ./load_mc.sh "$mc_client"

# return_value=$?

# if [ $return_value -eq 1 ]; then
#     exit 1
# fi

# task_id="test"
# bucket_path="${mc_client}/algorithm/input/01925967-7bfa-4091-ac3c-31b41d9f5fa5/origin.mha"
# output_file="nodule_det.json"

# signed_url=$(./mc share download $bucket_path --json | jq -r '.share')

# exec_env=$(jq -n \
#                 --arg task_id "$task_id" \
#                 --arg url "$signed_url" \
#                 --arg output "$output_file" \
#                 '{
#                     task_id: $task_id,
#                     input: [{url: $url}],
#                     output: $output
#                 }')

exec_env=$(jq -r '.nodule_det' exec_env.json)
minio_env=$(jq -r '.minio_env' exec_env.json)

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
-e MINIO_ENV="$minio_env" \
hanglok/nodule_detection:2023_12_6