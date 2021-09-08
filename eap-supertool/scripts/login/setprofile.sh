#!/bin/bash

where=0
if [[ "$1" == *"tr-central-preprod"* ]]; then where=1; PROFILE="tr-central-preprod"; fi
if [[ "$1" == *"tr-central-prod"* ]]; then where=1; PROFILE="tr-central-prod"; fi
if [ $where -eq 0 ]; then
  echo "Parameter '$1' passed is not known by change profile script $0"
else
  echo $PROFILE > ./data/aws_default_profile.txt
fi
