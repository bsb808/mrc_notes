#!/usr/bin/env python

import argparse
import os
import sys
import time
from itertools import cycle
import subprocess
import json

def status_iterator(token, groupid, terminate_str):
    # Loop while starting up.
    t0 = time.time()
    status_cmd = "curl -X GET -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/simulations/%s"%(token, groupid)
    status_str = ""
    chcycle = cycle(["-","/","-","\\"])
    while terminate_str not in status_str:
        p = subprocess.Popen(status_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status, err = p.communicate()
        #print status
        statusd = json.loads(status)
        newstatus_str = statusd['status']
        if newstatus_str == status_str:
            sys.stdout.write("\r")
        else:
            sys.stdout.write("\n")
        if "Address has been acquired." in newstatus_str:
            msg = "[%7.1f]\t Status <%s> uri <%s> %s"%(time.time()-t0, 
                                                         newstatus_str,
                                                         statusd['uri'],
                                                         chcycle.next())
        else:
            msg = "[%7.1f]\t Status <%s> %s"%(time.time()-t0, 
                                                newstatus_str,
                                                chcycle.next())
        sys.stdout.write(msg)
        sys.stdout.flush()
        
        status_str = newstatus_str
        time.sleep(2)
    

valid_commands = ['start', 'status', 'stop', 'stopall']

parser = argparse.ArgumentParser(description='Helper script for CloudSim REST calls.')
parser.add_argument('command', type=str, choices=valid_commands)

args = parser.parse_args()

token = os.environ.get('TOKEN')

if token is None:
    print "Must have an environmental value <TOKEN> with your Cloudsim access token in order to proceed"
    sys.exit(1)

image = "tfoote/test_novnc:main"

# File name for storing group ids
home = os.environ.get("HOME")
gid_fname = os.path.join(home,'.cloudsim_groupid')

if ( (args.command == 'stop') or args.command == 'status'):

    with open(gid_fname) as f:
        for line in f:
            pass
        groupid = line

    if args.command == 'stop':
        print("Stopping group id <%s>"%groupid)
        stop_cmd = "curl -X POST -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/stop/%s"%(token, groupid)
        p = subprocess.Popen(stop_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out
    status_iterator(token, groupid, "Address has been acquired.")

    
elif args.command == 'start':
    start_cmd = "curl -X POST -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/start -F \"image=%s\" -F \"name=npstest\""%(token, image)
    print "Starting new image"
    #print start_cmd
    p = subprocess.Popen(start_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    outd = json.loads(out)

    groupid = outd['Simulation']['groupid']

    # Save as a one line text file
    with open(gid_fname, 'a') as f:
        f.write(groupid +  "\n")
    print("Appended groupid <%s> to <%s>"%(groupid,gid_fname))

    status_iterator(token, groupid, "Address has been acquired.")

