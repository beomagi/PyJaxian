#!/bin/bash

AWS_DEFAULT_PROFILE=`cat ./data/aws_default_profile.txt`
AWS_DEFAULT_REGION=`cat ./data/aws_default_region.txt`

if [[ "$AWS_DEFAULT_PROFILE" == *"-prod"* ]]; then
    echo "<span style='color:yellow;background-color:#800000;'>current profile : ${AWS_DEFAULT_PROFILE}</span>"
else
    echo "current profile : $AWS_DEFAULT_PROFILE" 
fi

echo "current region : $AWS_DEFAULT_REGION"


creds=`cat ${HOME}/.aws/credentials | tr '\n' '|'  | sed 's_\[_\n\[_g' | grep $AWS_DEFAULT_PROFILE` 
expires=`echo "$creds" | awk -F '|' '{print $7}'` 
account=`echo "$creds" | awk -F '|' '{print $5}'` 
role=`echo "$creds" | awk -F '|' '{print $8}'`

echo "$role"
echo "$account"
echo ""
echo "$expires"
texpires=`echo $expires|awk -F '=' '{print $2}'| sed 's_^ __g'`
tnow=`date -u +"%Y-%m-%d %H:%M:%SZ"`
echo "Time Now: $tnow"
if [[ "$texpires" < "$tnow" ]]; then
	echo "<span style='color:red'>EXPIRED</span>"
fi
