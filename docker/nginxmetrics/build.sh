#!/usr/bin/env bash

mkdir -p tmp
cp ../../nginx/stackstate_checks/nginxmetrics/data/conf.yaml.docker.example ./tmp
cp ../../nginx/stackstate_checks/nginxmetrics/*.py ./tmp
docker build -t jdewinne/stsnginxmetrics:1.0.1 .