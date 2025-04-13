#!/bin/bash

docker build --no-cache --file Dockerfile.build --build-arg AGVERSION=$NEW_TAG --tag cpu_load_build .
docker run --rm -v $(pwd):/dist cpu_load_build
