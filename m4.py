#!/bin/python

import telnetlib
import subprocess, sys


#def signal_handler(sig, frame):
 #       print('You pressed Ctrl+C!')
#        sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C')
#signal.pause()

#class bcolors:
 #   MAGENTA = '\033[95m'
  #  NC = '\033[0m'

class bcolors:
    MAGENTA = '\033[95m'
    NC = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'

M = bcolors.MAGENTA
NOC = bcolors.NC
R = bcolors.RED
GR = bcolors.GREEN


hostname = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Please enter the UUT IP Address: ' + GR + '10.1.1.' + NOC )
select_platform = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Please Select the UUT Platform eg. [ ' + GR + 'C3X60M4' + NOC +' ] [ '+ GR  +'C460M4' + NOC +' ] [ '+ GR + 'C240M4' + NOC +' ] [ '+ GR +'C220M4'+ NOC +' ]: ')
print ('----------{' + M +' BIOS IMAGES LIST' + NOC +' }-----------')
subprocess.call('ls  /tftpboot/ | grep "' + select_platform + '-BIOS"| awk \'{$0="|\t"$0"\t|"}\'1', shell=True)
print ('-----------------------------------------')

bm = raw_input('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Please enter the BIOS Image: ')
user = ("root")
tn = telnetlib.Telnet('10.1.1.' + hostname)
tn.read_until("login: ")
print ('[' +  bcolors.MAGENTA + '+' + bcolors.NC + ']' " Connection established.")
tn.write(user + "\n")
tn.read_until("]$")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Linux prompt found.")
#tn.write('get_bios_version \| awk \'\{print " " "Backup BIOS Version:" " " \$4\}\' \| head -1\n')


#print tn.read_very_eager()
#print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' '')

#tn.write('get_bios_version\n')
#tn.set_debuglevel(1)
#time.sleep(5)
#tn_read = tn.read_all()
#print repr(tn_read)

#timeout = 2
#tn_read = tn.read_until('Backup', timeout)
#print repr(tn_read)



#tn.read_eager()
tn.write("\n")
tn.write("blade-power off\n")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Powering off the UUT.")
tn.read_until("[ Success ]")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " UUT is now is in power off state.")
tn.write("\n")
tn.read_until("]$")
tn.write("\n")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Executing the BIOS-UPDATE command inside the shell")
tn.write("bios-update -P -M -C -b -f -s -r 10.1.1.1 -u " + bm + "\n")
tn.read_until('[STATUS] = [ Image Download (0 %), OK ]')
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Image Downloaded (10 %), OK.')
tn.read_until('[STATUS] = [ Image Header Verification (0 %), OK ]')
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Image Verification done (21 %), OK.')
tn.read_until('[STATUS] = [ Image Signature Validate (0 %), OK ]')
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Image Signature Validate  (33 %), OK.')
tn.read_until('[STATUS] = [ Write Host Flash (0 %), OK ]')
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Writing Host Flash (49 %), OK.')
tn.read_until('[STATUS] = [ Erase Host Flash (50 %), OK ]')
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Erasing Host Flash (65 %), OK.')
tn.read_until('[STATUS] = [ Write Host Flash (75 %), OK ]')
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' ' Writing Host Flash (75 %), OK.')
tn.read_until("Install Done")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Install done.")
tn.write("\n")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Activating the BIOS image.")
tn.write("bios-update -a 0 -s\n")
tn.read_until("Activation Done")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Image activated.")
print ('[' + bcolors.MAGENTA + '+' + bcolors.NC + ']' " Update completed succesfully.")
tn.write("\n")

tn.write("exit\n")

