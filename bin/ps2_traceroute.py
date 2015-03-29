#! /usr/bin/python3

import os
import sys
import subprocess

date_cmdline = ['date']
traceroute_cmdline = ['traceroute', '-I']
TRACEPREF='    '
#SERVERS=['amspsn-liv-gw01.planetside2.com.', 'amspsn-liv-gw02.planetside2.com.', 'amspsn-liv-gw03.planetside2.com.', 'amspsn-liv-gw04.planetside2.com.']
SERVERS=['69.174.194.165', '69.174.194.166', '69.174.194.167', '69.174.194.168']
# See: https://soeissuetracker.com/browse/PS-709


def logOut(string, logfile):
  if string is None:
    string = ''
  print(string, file=logfile, flush=True)

def prep_traceOut(raw): # To have the traceroute output code-formatted in reddit.
  return TRACEPREF+raw.replace('\n', '\n'+TRACEPREF)

def main():
  if not os.getuid() == 0: # Need to be root for -I option for traceroot.
    print("Need to be root.", file=sys.stderr)
    sys.exit()
  
  logFile = open('/home/mw/logs/ps2_latency_log', 'a+')
  #logFile = sys.stdout

  logOut('\n\nLooking at latency for planetside 2 EU servers.', logFile)
  logOut(subprocess.check_output(date_cmdline, stdin=sys.stdin, stderr=sys.stderr, shell=False, universal_newlines=True), logFile)

  for host in SERVERS:
    try:
      logOut(prep_traceOut(subprocess.check_output(traceroute_cmdline+[host], stdin=sys.stdin, stderr=sys.stderr, shell=False, universal_newlines=True)), logFile)
    except KeyboardInterrupt:
      sys.exit()
  

if __name__ == "__main__":
    main()

