#!/usr/bin/python3
import sys
import base64
import boto3
import json
import os

rawparam=sys.argv[1]
alarmwinid=sys.argv[2]

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




client = boto3.client('cloudwatch')

response=client.describe_alarms(StateValue='ALARM',MaxRecords=100)
alarmarray=response.get('MetricAlarms')
while "NextToken" in response:
    response=client.describe_alarms(StateValue='ALARM',MaxRecords=100,NextToken=response["NextToken"])
    alarmarray+=response.get('MetricAlarms')

tableid=alarmwinid+"_table"
pretty="<table id='{}'>".format(tableid)
for alarm in alarmarray:
    alarm_name=alarm.get("AlarmName","")
    alarm_utime=str(alarm.get("StateUpdatedTimestamp",""))[:-9]
    col1="<td>"+alarm_name+"</td>"
    col2="<td>"+alarm_utime+"</td>"
    line="<tr>"+col1+col2+"</tr>"
    pretty+=line
pretty+="</table>"

print(pretty)
