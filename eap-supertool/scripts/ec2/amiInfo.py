#!/usr/bin/python3
import sys
import base64
import boto3
import json
import os

rawparam=sys.argv[2]
amiparam=sys.argv[1]

rawparams=base64.b64decode(rawparam).decode('UTF-8')
paramarray=rawparams.split("<br>")


profile=""
region=""
for param in paramarray:
    if "Profile" in param:
        profile=param.split(":")[1]
    if "Region" in param:
        region=param.split(":")[1]

os.environ['AWS_DEFAULT_PROFILE'] = profile
os.environ['AWS_DEFAULT_REGION'] = region




client = boto3.client('ec2')
response = client.describe_images(ImageIds=[amiparam])
pretty = json.dumps(response,default=str,indent="  ",sort_keys=True)
pretty=pretty.replace(" ","&nbsp;")

print(pretty)
