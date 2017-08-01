import sys,subprocess,os,time

cwd = os.getcwd()

with open(cwd+"/vpn_config","r") as f:
	host = f.readline()[:-1]
	usr = f.readline()[:-1]
	pw = f.readline()[:-1]
	

os.system("printf '"+usr+"\n"+pw+"\ny'|/opt/cisco/anyconnect/bin/vpn -s connect "+host)
try:
	while True:
		time.sleep(20)
		os.system("/opt/cisco/anyconnect/bin/vpn status")
except KeyboardInterrupt:
	print("\nDisconnecting:\n")
	os.system("/opt/cisco/anyconnect/bin/vpn disconnect")
