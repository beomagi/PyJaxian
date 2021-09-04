#!/usr/bin/env python3
import socketserver
import http.server
import sys
import time
import urllib
import json
import threading
import os
import binascii
import subprocess
import glob

threadlist={}
filelist=glob.glob(r'./pages/*') #globally permitted file list

def loadfile(filename):
    """load a file and return data"""
    try:
        with open(filename,"r") as fh:
            return fh.read()
    except:
        print("ERROR: "+str(sys.exc_info()[0]))
        return ""

def loadpage(pagename):
    """restricts loadfile to pages within a specific folder"""
    fullname="./pages"+pagename
    if fullname in filelist:
        return loadfile(fullname)
    print("you asked for {}".format(fullname))
    print(json.dumps(filelist,indent="  "))

def writetofile(astring, filename):
    with open(filename,"w") as fh:
       fh.write(astring) 

def randID():
     return binascii.b2a_hex(os.urandom(8)).decode('utf-8')

class Handler(http.server.BaseHTTPRequestHandler):
    '''   use our own handler functions '''

    def sendtextinfo(self, code, text, ctype):
        self.send_response(code)
        self.send_header('Content-type', ctype)
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
        ctype = "text/html"

        parsed_data = urllib.parse.urlparse(self.path)
        location=parsed_data.geturl().lower()

        message=""
        if location == "/":
            message=loadpage("/mainpage.html")
        for filestypes in [".css",".htm",".html",".js"]:
            if location.endswith(filestypes):
                message=loadpage(location)
                if filestypes==".css": ctype="text/css"
                if filestypes==".js": ctype="text/javascript"

        print(parsed_data.geturl())
        self.sendtextinfo(200,message,ctype)

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
