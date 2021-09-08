#!/bin/bash

where=0
if [[ "$1 $2" == *"eu-west-1"* ]]; then where=1; REGION="eu-west-1"; fi
if [[ "$1 $2" == *"emea"* ]]; then where=1; REGION="eu-west-1"; fi
if [[ "$1 $2" == *"us-east-1"* ]]; then where=1; REGION="us-east-1"; fi
if [[ "$1 $2" == *"amer"* ]]; then where=1; REGION="us-east-1"; fi
if [[ "$1 $2" == *"apac"* ]]; then where=1; REGION="ap-southeast-1"; fi
if [[ "$1 $2" == *"ap-southeast-1"* ]]; then where=1; REGION="ap-southeast-1"; fi
if [[ "$1 $2" == *"sing"* ]]; then where=1; REGION="ap-southeast-1"; fi
if [ $where -eq 0 ]; then
  echo "say emea, amer, apac, sing... I've no idea where to connect to"
else
  echo $REGION > ./data/aws_default_region.txt
fi

