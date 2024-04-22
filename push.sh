#!/bin/bash

docker images | grep "10.8.6.34:5000/algorithm" | awk '{print $1 ":" $2}' | while read image; do
    docker push $image
    print
done