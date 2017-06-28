#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)
peg fetch ${CLUSTER_NAME}
peg fetch ${CLUSTER_NAME}.db

## Now start up hdfs and spark services on the master (node 1) remotely
#peg sshcmd-node ${CLUSTER_NAME} 1 "source .profile && \$HADOOP_HOME/sbin/start-dfs.sh && \$SPARK_HOME/sbin/start-all.sh"

peg service ${CLUSTER_NAME} hadoop start
peg service ${CLUSTER_NAME} spark start
peg service ${CLUSTER_NAME} zookeeper start
echo "Starting kafka service..."
peg service ${CLUSTER_NAME} kafka start > /dev/null 2>&1 &
