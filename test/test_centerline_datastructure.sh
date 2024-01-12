#!/bin/bash

# mc_client="$1"

# ./load_mc.sh "$mc_client"

# return_value=$?

# if [ $return_value -eq 1 ]; then
#     exit 1
# fi

# task_id="test"
# bucket_path="${mc_client}/algorithm/output/7c7eb7c5-afd5-475e-ac65-154738f1901c/AirwaySegmentation-0.1.3-jcxiong/airwaysegmentation.nii.gz"
# output_file="Centerline_polyline.txt"

# signed_url=$(./mc share download $bucket_path --json | jq -r '.share')

exec_env=$(jq -r '.centerline_datastructure' exec_env.json)
minio_env=$(jq -r '.minio_env' exec_env.json)

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
-e MINIO_ENV="$minio_env" \
hanglok/centerline_datastructure:1023