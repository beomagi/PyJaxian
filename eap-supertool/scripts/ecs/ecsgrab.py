#!/usr/bin/python3
import sys
import base64
import boto3
import json
import os

rawparam=sys.argv[1]
ecswindow=sys.argv[2]

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






def ecsgather(region):
    client = boto3.client('ecs',region_name=region)
    clusters=[]
    response = client.list_clusters()
    clusters+=response.get("clusterArns",[])
    while response.get("nextToken"):
        response = client.list_clusters()
        clusters+=response.get("clusterArns",[])
    return clusters

def ecsorganize(data):
    retlines=[]
    tableID=ecswindow+"_table"
    retlines.append("<table id='"+tableID+"'>")
    col1="<th>Cluster ARN list</th>"
    line="<tr>"+col1+"</tr>"
    retlines.append(line)
    for cluster in data:
        col1="<td><div class='smoldyn' onclick=\"SendAndCallback('script|ecs/ecsARN.py|"+cluster+"|"+ecswindow+"|"+rawparam+"',ecsInfoWindow)\">"+cluster+"</div></td>"
        line="<tr>"+col1+"</tr>"
        retlines.append(line)
    retlines.append("</table>")
    rethtml="\n".join(retlines)
    return rethtml




data=ecsgather(region);

formatteddata=ecsorganize(data)
print(formatteddata.replace("\n",""))
