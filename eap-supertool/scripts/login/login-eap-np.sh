#!/bin/bash
. ~/bashfuncs/run_awsfuncs.sh
awslogineapnonprod `cat ./data/aws_default_region.txt`
export AWS_DEFAULT_PROFILE=tr-central-preprod
echo "$AWS_DEFAULT_PROFILE" > ./data/aws_default_profile.txt
