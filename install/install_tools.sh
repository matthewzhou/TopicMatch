#!/bin/bash
## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)
peg fetch ${CLUSTER_NAME}
peg fetch ${CLUSTER_NAME}.db

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} hadoop
peg install ${CLUSTER_NAME} spark
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka


peg sshcmd-node ${CLUSTER_NAME} 1 "sudo pip install kafka-python"
