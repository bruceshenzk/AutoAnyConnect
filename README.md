# Introduction
If you have been using the Cisco Anyconnect client with NYU VPN (or maybe VPN of other universities), you must type in password everytime you log in. This program can eventually save you a lot of time from the repetitive task by using the command line use of the Cisco Anyconnect.

The program is created under an [answer](https://superuser.com/questions/649614/connect-using-anyconnect-from-command-line) that we found online. 

** It only works on Mac for now **

# Usage
* Make sure that you have python installed on your Mac
* Download and install Cisco Anyconnect.
* Check if binary /opt/cisco/anyconnect/bin/vpn exists.
* Setup your config file with correct HOST, USERNAME and PASSWORD
```
echo "HOST\nUSERNAME\nPASSWORD" > vpn_config
```
* Start the program by entering `python aac.py`
* Stop by hitting Ctrl + C, and wait for the program to disconnecting the VPN service.

# Works under Development
Multiple config files
