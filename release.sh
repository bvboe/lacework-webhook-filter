#!/bin/bash

cd `dirname "$0"`
rm -rf build
./build.sh

aws s3 cp ./LaceworkWebhookFilter.yaml s3://bboe-lambda-code/lacework-webhook-filter/LaceworkWebhookFilter.yaml --acl public-read
aws s3 cp ./build/deployment-package.zip s3://bboe-lambda-code/lacework-webhook-filter/deployment-package.zip --acl public-read
