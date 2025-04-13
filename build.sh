#!/bin/bash

docker build --no-cache --file Dockerfile.build --tag hetznersnapshot2_build .
docker run --rm -v $(pwd):/dist hetznersnapshot2_build
