#!/usr/bin/env python3
import socketserver
import http.server
import sys
import time
import urllib
import json
import boto3
import threading
import os
import binascii
import subprocess

threadlist={}

ec2filters={}


def ec2gather():
    client = boto3.client('ec2')
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
    with open ("./data/ec2-all.json","w") as df:
        df.write(json.dumps(ec2_all,indent="  ",default=str))


def loadpage(pagename):
    with open("./pages/"+pagename+".html","r") as ph:
        return ph.read()
    return ""

def loadfile(filename):
    with open(filename,"r") as fh:
        return fh.read()

def writetofile(astring, filename):
    with open(filename,"w") as fh:
       fh.write(astring) 

def randID():
     return binascii.b2a_hex(os.urandom(5)).decode('utf-8')


def ctlogin(ip):
    """
    tmux new-window -k "export AWS_DEFAULT_REGION=us-east-1;cloud-tool --profile tr-central-preprod ssh --private-ip  10.97.110.49; sleep 1"
    """
    print("spawning!")
    windowname="bastion-"+ip
    subprocess.Popen("tmux new-window -n "+windowname+" -k \"export AWS_DEFAULT_REGION=us-east-1;cloud-tool --profile tr-central-preprod ssh --private-ip  "+ip+"; sleep 1\"",shell=True,close_fds=True)



def ec2organize(filterid):
    tdata=loadfile("./data/ec2-all.json")
    try:
        jdata=json.loads(tdata)
    except:
        return "ERROR: "+str(sys.exc_info()[0])
    retlines=[]
    retlines.append("<table>")
    for instanceinfo in jdata:
        ec2id=instanceinfo["InstanceId"]
        ec2ippriv=instanceinfo.get("PrivateIpAddress","")
        ec2ami=instanceinfo["ImageId"]
        ec2tags=instanceinfo["Tags"]
        ec2name=""
        for kv in ec2tags:
            if kv.get("Key","")=="Name":
                ec2name=kv.get("Value")
        line="<tr><td>"+ec2id+"</td><td>"+ec2name+"</td><td><div class='smoldyn' onclick=\"svrupdate('loginto_"+ec2ippriv+"')\">"+ec2ippriv+"<div></td><td>"+ec2ami+"</tr>"
        if filterid=="":
            retlines.append(line)
        else:
            if ec2filters.get(filterid,"") in line:
                retlines.append(line)
    retlines.append("</table>")
    retdata="\n".join(retlines)
    return retdata


def collectdetails():
    region=os.environ.get("AWS_DEFAULT_REGION")
    profile=os.environ.get("AWS_DEFAULT_PROFILE")
    if profile == "tr-central-prod":
        profile="<span class='warning'>tr-central-prod</span>"
    lines=[]
    lines.append("Region :"+region)
    expiry=""
    if "tr-central-preprod" in profile:
        expiry=subprocess.check_output("./scripts/aws_preprod_expiry.sh 2>&1", shell=True, text=True)
    if "tr-central-prod" in profile:
        expiry=subprocess.check_output("./scripts/aws_prod_expiry.sh 2>&1", shell=True, text=True)
    tnow=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
    lines.append("Profile :"+profile+" &emsp;&emsp; expires: "+expiry+" &emsp; Now: "+tnow)
    return "<br/>".join(lines)


class Handler(http.server.BaseHTTPRequestHandler):
    '''   use our own handler functions '''

    def sendtextinfo(self, code, text):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if type(text)==type([]):
            for lines in text:
                self.wfile.write((str(lines)+"\n").encode())
        else:
            self.wfile.write((str(text)+"\n").encode())

    def do_GET(self):
        '''   handle get   '''
        tnow = time.time()
        gnow = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(tnow)) #Formatted UTC time

        parsed_data = urllib.parse.urlparse(self.path)
        location=parsed_data.geturl().lower()

        message=""
        if location == "/":
            message=loadpage("eapst-main")

        if location == "/loginnonprod":
            output=subprocess.check_output("./scripts/eap-login-np.sh emea 2>&1", shell=True, text=True)
            message=output.replace("\n","<br/>")

        if location == "/loginprod":
            output=subprocess.check_output("./scripts/eap-login-p.sh emea 2>&1", shell=True, text=True)
            message=output.replace("\n","<br/>")

        if location == "/ec2":
            message=loadpage("ec2")
            message=message.replace("#IDREP1#",randID())

        if location.startswith("/ec2instances_"):
            filterid=location.split("_")[1]
            message=ec2organize(filterid)
        
        if location.startswith("/loginto_"):
            serverip=location.split("_")[1]
            ctlogin(serverip)

        if location.startswith("/ec2gather_"):
            writetofile("./data/ec2-all.json","gathering")
            ec2gatherthread=threading.Thread(target=ec2gather, name="EC2Gather")
            threadlist["EC2Gather"]=ec2gatherthread
            ec2gatherthread.start()

        if location.startswith("/setregion_"):
            regioncode=location.split("_")[1]
            if regioncode=="amers": region="us-east-1"
            if regioncode=="emea": region="eu-west-1"
            if regioncode=="sing": region="ap-southeast-1"
            os.environ["AWS_DEFAULT_REGION"]=region

        if location.startswith("/setprofile_"):
            profilecode=location.split("_")[1]
            if profilecode=="preprod":
                profileset="tr-central-preprod"
            if profilecode=="realprod":
                profileset="tr-central-prod"
                message="BE WARNED, THIS IS PRODUCTION!"
            os.environ["AWS_DEFAULT_PROFILE"]=profileset


        if location.startswith("/ec2filter_"):
            filterid=location.split("_")[1]
            filtertext=location.split("_")[2]
            ec2filters[filterid]=filtertext

        if location.startswith("/getmaindetails"):
            message=collectdetails()

        print(parsed_data.geturl())
        self.sendtextinfo(200,message)

    def do_POST(self):
        '''   handle post like rest API   '''
        try: #try getting the bytestream of the request
            content_length = int(self.headers['Content-Length'])
            print(content_length)
        except Exception as err:
            print("malformed headers")
            self.sendtextinfo(200,str(err))
            return

        if content_length > 0:
            rawrequest = self.rfile.read(content_length).decode('utf-8')
            print("Received POST: {}".format(rawrequest))
            try:
                jrequest = json.loads(rawrequest)
            except Exception as err:
                pass
        else:
            jrequest=None
        print(jrequest)

        return


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    '''    Basic threaded server class    '''
    http.server.HTTPServer.request_queue_size = 128

if sys.argv[1:]:
    HTPORT = int(sys.argv[1])
else:
    HTPORT = 8000

HTSERVER = ThreadedHTTPServer(('', HTPORT), Handler)

try:
    while 1:
        sys.stdout.flush()
        HTSERVER.handle_request()
except KeyboardInterrupt:
    print("Server Stopped")
