#!/usr/bin/env bash

mkdir -p tmp
cp ../nginx/stackstate_checks/nginxtopo/data/conf.yaml.docker.example ./tmp
cp ../nginx/stackstate_checks/nginxtopo/*.py ./tmp
docker build -t jdewinne/stsnginxtopo .