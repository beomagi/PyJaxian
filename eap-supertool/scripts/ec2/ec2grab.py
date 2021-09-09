#!/usr/bin/python3
import sys
import base64
import boto3
import json
import os

rawparam=sys.argv[1]
ec2window=sys.argv[2]

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






def ec2organize(jdata,filterid):
    retlines=[]
    tableID=ec2window+"_table"
    retlines.append("<table id='"+tableID+"'>")
    for instanceinfo in jdata:
        ec2id=instanceinfo["InstanceId"]
        ec2ippriv=instanceinfo.get("PrivateIpAddress","")
        ec2ami=instanceinfo["ImageId"]
        ec2tags=instanceinfo.get("Tags",[])
        ec2launchtime=str(instanceinfo.get("LaunchTime",""))
        ec2state=instanceinfo.get("State",{}).get("Name","")
        ec2name=""
        for kv in ec2tags:
            if kv.get("Key","")=="Name":
                ec2name=kv.get("Value")
        col1="<td>"+ec2id+"</td>"
        col2="<td>"+ec2name+"</td>"
        col25="<td>"+ec2state+"</td>"
        col3="<td><div class='smoldyn' onclick=\"SendAndCallback('loginto|"+ec2ippriv+"')\">"+ec2ippriv+"<div></td>"
        col4="<td><div class='smoldyn' onclick=\"SendAndCallback('script|ec2/amiInfo.py|"+ec2ami+"|"+rawparam+"',ec2AMIwindow)\">"+ec2ami+"</div></td>"
        col5="<td>"+ec2launchtime+"</td>"
        line="<tr>"+col1+col2+col25+col3+col4+col5+"</tr>"
        if filterid=="":
            retlines.append(line)
        else:
            if ec2filters.get(filterid,"") in line:
                retlines.append(line)
    retlines.append("</table>")
    retdata="\n".join(retlines)
    return retdata

def ec2gather(region):
    client = boto3.client('ec2',region_name=region)
    response = client.describe_instances()
    ec2_all=[]
    for reservation in response["Reservations"]:
        instances=reservation["Instances"]
        ec2_all+=instances
    nexttoken=response.get("NextToken")
    while nexttoken != None:
        response = client.describe_instances(NextToken=nexttoken)
        instances=reservation["Instances"]
        ec2_all+=instances
    return ec2_all



data=ec2gather(region);

formatteddata=ec2organize(data,"")
print(formatteddata.replace("\n",""))
