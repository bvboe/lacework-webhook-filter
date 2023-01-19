#!/bin/bash

cd `dirname "$0"`
mkdir -p build
cd build
rm -rf src
cp -r ../src .

cd src
pip install \
    --platform manylinux2014_x86_64 \
    --target=. \
    --implementation cp \
    --python 3.9 \
    --only-binary=:all: --upgrade \
    requests

zip -r ../deployment-package.zip .
