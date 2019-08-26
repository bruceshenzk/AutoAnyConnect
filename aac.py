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
    
    # turn on Cisco Anyconnect VPN
    #os.system("printf '"+usr+"\n"+pw+"\ny'|/opt/cisco/anyconnect/bin/vpn -s connect "+host)
    p = subprocess.Popen("/opt/cisco/anyconnect/bin/vpn -s connect " + host, shell=True,
            stdout=None, stdin=subprocess.PIPE)

    time.sleep(2)
    print("sending usr")
    p.stdin.write(usr+'\n')
    
    time.sleep(2)
    print("sending pw")
    p.stdin.write(pw+'\n')
    
    time.sleep(2)
    print("sending confirm")
    p.stdin.write('y\n')

    p.wait()

    # keep process alive and check connecting state regularly
    try:
            while True:
                    time.sleep(20)
                    output = str(subprocess.Popen("/opt/cisco/anyconnect/bin/vpn status", shell=True, stdout=subprocess.PIPE).stdout.read())
                    if ">> state: Disconnected" in output:
                            print(">> Disconnected")
                    elif ">> state: Connected" in output:
                            print(">> Connected")
                    else:
                            print(">> Other")
                            print(output)

    # Ctrl + C to disconnect
    except KeyboardInterrupt:
            print("\nDisconnecting:\n")
            p = subprocess.Popen("/opt/cisco/anyconnect/bin/vpn disconnect", shell=True)
            p.wait()
    

if __name__ == "__main__" :
    sys.exit(main())


