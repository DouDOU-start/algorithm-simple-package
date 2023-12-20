#!/bin/bash

exec_env=$(jq -r '.fusion' exec_env.json)

docker run --rm --shm-size=1g \
-e EXEC_ENV="$exec_env" \
hanglok/fusion:0.0.1