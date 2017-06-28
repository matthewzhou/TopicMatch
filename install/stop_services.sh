#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)
peg fetch ${CLUSTER_NAME}
peg fetch ${CLUSTER_NAME}.db

## stop tools, in reverse order of 03start_tools.sh

peg service ${dna}-db redis stop
peg service ${CLUSTER_NAME} kafka stop
peg service ${CLUSTER_NAME} zookeeper stop
peg service ${CLUSTER_NAME} spark stop
peg service ${CLUSTER_NAME} hadoop stop

