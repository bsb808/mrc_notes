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
    t1 = t0
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
            t1 = time.time()
        if "running" in newstatus_str:
            msg = "[%7.1f, %7.1f]\t Status <%s> uri <%s> %s"%(time.time()-t0,
                                                              time.time()-t1,
                                                              newstatus_str,
                                                              statusd['uri'],
                                                              chcycle.next())
        else:
            msg = "[%7.1f, %7.1f]\t Status <%s> %s"%(time.time()-t0,
                                              time.time()-t1,
                                              newstatus_str,
                                              chcycle.next())
        sys.stdout.write(msg)
        sys.stdout.flush()
        
        status_str = newstatus_str
        time.sleep(2)
        
    sys.stdout.write("\n")
    sys.stdout.flush()
    

valid_commands = ['start', 'status', 'stop', 'stopall']

parser = argparse.ArgumentParser(description='Helper script for CloudSim REST calls.')
parser.add_argument('command', type=str, choices=valid_commands)

args = parser.parse_args()

# Image name
#image = "tfoote/test_novnc:main"
#name = "npstest"

image = "learninglab/me4823:matlab_small"
name = "4823matlabsmall"

#image = "learninglab/me4823:main"
#name = "4823main"

# Get token from file
home = os.environ.get("HOME")
token_fname = os.path.join(home,'.cloudsim_token')
if not os.path.isfile(token_fname):
    print "You need to save your cloudsim token as the file <%s>"%token_fname
    sys.exit(1)

with open(token_fname) as f:
    token = f.readline().strip()

print "Using access token <%s>"%(token)

# File name for storing group ids
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
    status_iterator(token, groupid, "running")

elif args.command == 'stopall':
    print ("Stopping all images..")
    stopall_cmd = "curl -X POST -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/stop/all"%token
    print stopall_cmd
    p = subprocess.Popen(stopall_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    if os.path.isfile(gid_fname):
        print ""
        print "Removing file <%s>"%gid_fname
        os.remove(gid_fname)

    
elif args.command == 'start':
    start_cmd = "curl -X POST -H \"Private-Token: %s\" https://staging-cloudsim-nps.ignitionrobotics.org/1.0/start -F \"image=%s\" -F \"name=%s\""%(token, image, name)
    print "Starting new image"
    #print start_cmd
    p = subprocess.Popen(start_cmd, shell=True, executable='/bin/bash' ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    outd = json.loads(out)

    success = False
    try:
        groupid = outd['Simulation']['groupid']
        success = True
    except KeyError:
        print("WARNING:  Looks ike the simulation didn't start!")

    if success:
        # Save as a one line text file
        with open(gid_fname, 'a') as f:
            f.write(groupid +  "\n")
        print("Appended groupid <%s> to <%s>"%(groupid,gid_fname))
        
        status_iterator(token, groupid, "running")

