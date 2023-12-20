#!/bin/bash

exec_env=$(jq -r '.nodule_det' exec_env.json)

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
hanglok/nodule_detection:2023_12_6