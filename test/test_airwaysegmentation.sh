#!/bin/bash

exec_env=$(jq -r '.airwaysegmentation' exec_env.json)

docker run --rm --shm-size=1g --gpus 1 \
-e EXEC_ENV="$exec_env" \
hanglok/airwaysegmentation:0.1.3