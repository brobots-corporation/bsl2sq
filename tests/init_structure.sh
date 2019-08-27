#!/bin/bash

set -euv 

ROOT_DIR=$(pwd)
NAME_TEST_STR_ARCH='conf.tar.gz'

cd ./tests

tar -xzf $NAME_TEST_STR_ARCH
TEST_DIR=$(pwd)
chmod -R 777 $TEST_DIR

cd $ROOT_DIR