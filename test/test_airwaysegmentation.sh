#!/bin/bash

mc_client="$1"

./load_mc.sh "$mc_client"

return_value=$?

if [ $return_value -eq 1 ]; then
    exit 1
fi

task_id="test"
bucket_path="${mc_client}/algorithm/input/0ca9859e-255b-407b-b33f-4560ec2d95d7.mha"
output_file="airwaysegmentation.nii.gz"

signed_url=$(./mc share download $bucket_path --json | jq -r '.share')

exec_env=$(jq -n \
                --arg task_id "$task_id" \
                --arg url "$signed_url" \
                --arg output "$output_file" \
                '{
                    task_id: $task_id,
                    input: [{url: $url}],
                    output: $output
                }')

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
hanglok/airwaysegmentation:0.1.3