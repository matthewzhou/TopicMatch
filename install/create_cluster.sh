#!/bin/bash

## read in cluster name from config file
CLUSTER_NAME=$(<00cluster_name.txt)

## get this script's location, from http://stackoverflow.com/questions/59895/
MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
peg up ${MYDIR}/master.yml &
peg up ${MYDIR}/workers.yml &
peg up ${MYDIR}/db.yml &
