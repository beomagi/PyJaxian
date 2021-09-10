#!/usr/bin/python3
import sys
import base64
import boto3
import json
import os

clusterARN=sys.argv[1]
ecswindow=sys.argv[2]
rawparam=sys.argv[3]
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
    response = client.describe_clusters(clusters=[clusterARN])
    clusterdata=response.get("clusters")
    if len(clusterdata)>0:
        return clusterdata[0]
    else:
        return None

def ecsorganize(data):
    servicetableid=ecswindow+"_svctable"
    clusterARN=data["clusterArn"]
    clusterName=data["clusterName"]
    clusterinstances=data["registeredContainerInstancesCount"]
    clustertasks=data["runningTasksCount"]

    client = boto3.client('ecs',region_name=region)
    servicelist = client.list_services(cluster=clusterARN,maxResults=100)
    svclist=servicelist.get("serviceArns",[])
    while servicelist.get("nextToken"):
        servicelist = client.list_services(cluster=clusterARN,maxResults=100,nextToken=servicelist.get("nextToken"))
        svclist+=servicelist.get("serviceArns",[])


    client = boto3.client('ecs',region_name=region)
    
    servicetable=[]
    servicetable.append("<table id='{}'>".format(servicetableid))

    line=""
    line+="<tr>" 
    line+="<th>Arn</th>"
    line+="<th>Name</th>"
    line+="<th>Status</th>"
    line+="<th>Desired</th>"
    line+="<th>Running</th>"
    line+="<th>Pending</th>"
    line+="<th>Definition</th>"
    line+="</tr>"
    servicetable.append(line)


    while len(svclist) >0:
        checklist=svclist[0:10]
        svclist=svclist[10:]
        servicesresponse = client.describe_services(cluster=clusterARN,services=checklist)

        for aservice in servicesresponse.get("services",[]):
            serviceArn = aservice["serviceArn"]
            serviceName = aservice["serviceName"]
            serviceStatus = aservice["status"]
            svcdesired = str(aservice["desiredCount"])
            svcrunning = str(aservice["runningCount"])
            svcpending = str(aservice["pendingCount"])
            svcdefn = aservice["taskDefinition"]

            line=""
            line+="<tr>" 
            line+="<td>"+serviceArn+"</td>"
            line+="<td>"+serviceName+"</td>"
            line+="<td>"+serviceStatus+"</td>"
            line+="<td>"+svcdesired+"</td>"
            line+="<td>"+svcrunning+"</td>"
            line+="<td>"+svcpending+"</td>"
            line+="<td>"+svcdefn+"</td>"
            line+="</tr>"
            servicetable.append(line)

    servicetable.append("</table>")
    rehtml=json.dumps(data,indent="  ",default=str,sort_keys=True).replace("\n","<br>").replace(" ","&nbsp;")
    rehtml+="<br>"
    rehtml+= "".join(servicetable)
    return rehtml




clusterdata=ecsgather(region)
if (clusterdata != None):
    formatteddata=ecsorganize(clusterdata)
else:
    formatteddata="No data for this cluster"
print(formatteddata.replace("\n",""))
