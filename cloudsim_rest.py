#!/usr/bin/env python

import argparse
import os
import sys
import time
import subprocess
import json

valid_commands = ['start', 'status', 'stop', 'stopall']

parser = argparse.ArgumentParser(description='Setup NPS workspaces')
parser.add_argument('command', type=str, choices=valid_commands)

args = parser.parse_args()

token = os.environ.get('TOKEN')

if token is None:
    print "Must have an environmental value <TOKEN> with your Cloudsim access token in order to proceed"
    sys.exit(1)

image = "tfoote/test_novnc:main"
if args.command == 'start':
    start_cmd = "curl -X POST -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/start -F \"image=%s\" -F \"name=npstest\""%(token, image)
    print "Starting new image"
    #print start_cmd
    p = subprocess.Popen(start_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    outd = json.loads(out)
    groupid = outd['Simulation']['groupid']

    # Save as an env
    gvar = "GROUPID"
    cnt = 0
    while os.environ.get(gvar) is not None:
        print("Looks like you already have an env <%s> set as <%s>"
              %(gvar, os.environ.get(gvar)))
        gvar = "GROUPID%d"%cnt
        cnt += 1
    os.environ[gvar] = groupid
    print("Exported groupid <%s> as env <%s>"%(groupid,gvar))

    # Loop while starting up.
    t0 = time.time()
    status_cmd = "curl -X GET -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/simulations/%s"%(token,groupid)
    status_str = ""
    while "Address has been acquired." not in status_str:
        p = subprocess.Popen(status_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status, err = p.communicate()
        #print status
        statusd = json.loads(status)
        status_str = statusd['status']
        print("[%7.2f]\t Status: %s"%(time.time()-t0, status_str))
        time.sleep(2.0)
                                   
                                        

