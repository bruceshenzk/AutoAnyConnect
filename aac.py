#! /usr/bin/python
from __future__ import print_function
import sys,subprocess,os,time

config_file = "vpn_config"
cwd = os.getcwd()

# Check the config argument
if len(sys.argv) > 1:
	if os.path.isfile(cwd+"/"+sys.argv[1]):
		config_file = sys.argv[1]
	else:
		print("Config file does not exist!")
print("Using config file: " + config_file)

# read for credentials
with open(cwd+"/"+config_file,"r") as f:
	host = f.readline()[:-1]
	usr = f.readline()[:-1]
	pw = f.readline()[:-1]
	

# turn on Cisco Anyconnect VPN
os.system("printf '"+usr+"\n"+pw+"\ny'|/opt/cisco/anyconnect/bin/vpn -s connect "+host)

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
	os.system("/opt/cisco/anyconnect/bin/vpn disconnect")
