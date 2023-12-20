#!/bin/bash

exec_env=$(jq -r '.centerline_datastructure' exec_env.json)

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
hanglok/centerline_datastructure:1023