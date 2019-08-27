#!/usr/bin/python
from __future__ import print_function
import sys,subprocess,os,time
import argparse
import logging
logger = logging.getLogger("Auto-Anycisco-Connect")
logger.setLevel("DEBUG")

parser = argparse.ArgumentParser()
parser.add_argument("config", action='store')
args = parser.parse_args()

def disconnect():
    p = subprocess.Popen(["/opt/cisco/anyconnect/bin/vpn", "disconnect"])
    p.wait()

def send_until(p, cmd, exp, st):
    #print("send_until")

    s = ''
    line = ''
    cnt = 1
    while True:

        while True:
            c = p.stdout.read(1)
            if c == '\x0a' or c == '\x0d':
                line = s
                s = ''
                break
            else:
                s += c
                if st in s:
                    p.stdin.write(cmd)
                    return

        print("Line %d: \'%s\'" % (cnt, line))
        if exp in line:
            found_exp = True
        cnt+=1

def main():
    if os.path.exists(args.config):
        logger.info("Using config file", args.config)
    else:
        logger.warning("Not valid config")
        return 1
    
    # read for credentials
    with open(args.config,"r") as f:
            host = f.readline()[:-1]
            usr = f.readline()[:-1]
            pw = f.readline()[:-1]

    disconnect()

    # turn on Cisco Anyconnect VPN
    p = subprocess.Popen(["/opt/cisco/anyconnect/bin/vpn", "-s"],
            stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    send_until(p, "connect %s\n" % host, "registered", "VPN> ")
    send_until(p, "%s\n" % usr, "", "Username:")
    send_until(p, "%s\n" % pw, "", "Password:")
    send_until(p, "y\n", "", "accept?")
    time.sleep(5)

    # keep process alive and check connecting state regularly
    try:
        while True:
            p.stdin.write("status\n")
            line = p.stdout.readline()
            while "state" not in line:
                line = p.stdout.readline()
            print(line)
            time.sleep(20)

    # Ctrl + C to disconnect
    except KeyboardInterrupt:
        disconnect()
    

if __name__ == "__main__" :
    sys.exit(main())


