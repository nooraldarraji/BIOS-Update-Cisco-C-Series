#!/bin/python
import telnetlib
import subprocess, sys
import os

class bcolors:
    MAGENTA = '\033[95m'
    NC = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'

M = bcolors.MAGENTA
NOC = bcolors.NC
R = bcolors.RED
GR = bcolors.GREEN
hostname = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Please enter the UUT IP Address: ' + GR + '10.1.1.' + NOC)
select_platform = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Please Select the UUT Platform eg. [ ' + GR + 'S3X60M5' + NOC +' ] [ '+ GR  +'C480M5' + NOC +' ] [ '+ GR + 'C240M5' + NOC +' ] [ '+ GR +'C220M5'+ NOC +' ]: ')
print ('----------{' + M +' BIOS IMAGES LIST' + NOC +' }-----------')
subprocess.call('ls  /tftpboot/ | grep "' + select_platform + '-BIOS"| awk \'{$0="|\t"$0"\t|"}\'1', shell=True)
print ('-----------------------------------------')

bm = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Enter BIOS Image: ')
user = ("root")
tn = telnetlib.Telnet('10.1.1.' + hostname)

tn.read_until("login: ")
print ('[' +  M + '+' + NOC + ']' ' Connection Established.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
tn.write(user + "\n")
tn.read_until("]$")
print ('[' + M + '+' + NOC + ']' ' Linux prompt found.\t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')

tn.write("\n")
tn.write("blade-power off\n")
print ('[' + M + '+' + NOC + ']' ' Powering off the UUT.\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
tn.read_until("[ Success ]")
print ('[' + M + '+' + NOC + ']' ' UUT is now is in power off state. \t\t\t [ ' + GR + 'OK' + NOC +' ]')
tn.write("\n")
tn.read_until("]$")
tn.write("\n")
print ('[' + M + '+' + NOC + ']' ' Executing the BIOS-UPDATE command inside the shell.   [ ' + GR + 'OK' + NOC +' ]')
tn.write("bios-update -P -M -C -b -f -s -r 10.1.1.1 -u " + bm + "\n")
tn.read_until('[STATUS] = [ Image Download (0 %), OK ]')

sp_to = 3
sp_error_msg = ('Validation Failed, rc=36')

print ('[' + M + '+' + NOC + ']' ' Downloading Image (10 %). \t \t\t\t [ ' + GR + 'OK' + NOC +' ]')
nf_to = 3
nf_error_msg = ('Error code 1: File not found')
try:
    nf_error_check = tn.read_until((nf_error_msg), nf_to)
except EOFError as e:
    print "Connection is not poor: %s" % e
  
if ((nf_error_msg) in (nf_error_check)):
    print ('[' + R + '+' + NOC + ']' ' File Not Found! \t\t\t\t\t [' + R + ' CHECK FILE NAME' + NOC + ' ]')
    tn.write("exit\n")
    sys.exit()
else:
    tn.read_until('[STATUS] = [ Image Signature Validate (0 %), OK ]')
#try:
#   platform_error_check = tn.read_until((sp_error_msg), sp_to)
#except EOFError as s:

#if ((sp_error_msg) in (platform_error_check)):
#    print ('[' + R + '+' + NOC + ']' ' Validation Failed, rc=36 \t\t\t\t [' + R + ' ERROR!' + NOC + ' ]')
#    tn.write("exit\n")
#    sys.exit()
    #else:
    print ('[' + M + '+' + NOC + ']' ' Image Signature Validate (20 %). \t\t\t [ ' + GR + 'OK' + NOC +' ]')
    tn.read_until('[STATUS] = [ Image Header Verification (0 %), OK ]')
    print ('[' + M + '+' + NOC + ']' ' Image Header Verification (41 %). \t\t\t [ ' + GR + 'OK' + NOC +' ]')

    # The reason for a seperate Timeout variable is because each failure fail slower than the other, so i keep it like that in case of a change.

    pf_to = 3
    pf_error_msg = ('[STATUS] = [ Error, Image not for this platform ]')
    hw1_to = 3
    hw1_error_msg = ('[STATUS] = [ Error, CPU ID file read failed ]')
    hw2_to = 3
    hw2_error_msg = ('[STATUS] = [ Error, CPU ID mis-match between uploaded image and the platform ]')
    hw_all_to = 3
    hw_all_error_msg = ('[STATUS] = [ Error,')
    try:
         platform_error_check = tn.read_until((pf_error_msg), pf_to)
    except EOFError as n:
        print "Image not matching the platform: %" % n
    if ((pf_error_msg) in (platform_error_check)):
        print ('[' + R + '+' + NOC + ']' ' Image Verification error \t\t\t\t [' + R + ' This Image is not for this Platform!' + NOC + ' ]')
        tn.write("exit\n")
        sys.exit()
        platform_error_check = tn.read_until((hw1_error_msg), hw1_to)
    elif ((hw1_error_msg) in (platform_error_check)):
        print ('[' + R + '+' + NOC + ']' ' CPU ID cannot be found! \t\t\t\t [' + R + ' Possible Hardware Error!' + NOC + ' ]') 
        tn.write("exit\n")
        sys.exit()
        platform_error_check = tn.read_until((hw2_error_msg), hw2_to)
    elif ((hw2_error_msg) in (platform_error_check)):
        print ('[' + R + '+' + NOC + ']' ' CPU ID mis-match between uploaded image and the platform! \t\t [' + R + ' Possible Hardware Error!' + NOC + ' ]')
        tn.write("exit\n")
        sys.exit()
        platform_error_check = tn.read_until((hw_all_error_msg), hw_all_to)
    elif ((hw_all_error_msg) in (platform_error_check)):
        print ('[' + R + '+' + NOC + ']' ' Error accrued during BIOS Update \t\t\t\t [' + R + ' Possible Hardware Error!' + NOC + ' ]') 
        tn.write("exit\n")
        sys.exit()
    else: 
        tn.read_until('[STATUS] = [ Write Host Flash (50 %), OK ]')
        print ('[' + M + '+' + NOC + ']' ' Write Host Flash (90 %). \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
        tn.read_until("Install Done")
        print ('[' + M + '+' + NOC + ']' ' Install done. \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
        tn.write("\n")
        print ('[' + M + '+' + NOC + ']' ' Activating the BIOS image. \t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
        tn.write("bios-update -a 0 -s\n")
        tn.read_until('Activation Done')
        print ('[' + M + '+' + NOC + ']' ' Image activated. \t\t\t\t\t [ ' + GR + 'OK' + NOC +' ]')
        print ('[' + M + '+' + NOC + ']' ' Firmware Update completed successfully. \t\t [ ' + GR + 'OK' + NOC +' ]')
        tn.write("\n")
        tn.write("exit\n")
