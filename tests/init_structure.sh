#!/bin/bash

set -euv 

NAME_TEST_STR_ARCH='conf.tar.gz'

mkdir -p ./test_src
cd ./test_src

tar -xzf $NAME_TEST_STR_ARCH
root_dir=$(pwd)
chmod -R 777 $root_dir