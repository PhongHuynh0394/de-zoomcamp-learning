#!bin/bash

export HADOOP_PREFIX=/usr/local/hadoop

$HADOOP_PREFIX/bin/hdfs dfs "$@"
