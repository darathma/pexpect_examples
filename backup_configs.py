import getpass
import pexpect
import sys
from datetime import date

user = input('Enter your username: ')
password = getpass.getpass()
ssh_newkey = 'Are you sure you want to continue connecting'
today = date.today()


file = open('multi_switches.txt', mode = 'r')

for host in file:
    IP = host.strip()
    print('Connecting to ' + (IP))
    tnconn = pexpect.spawn('ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 {}@{}'.format(user, IP), timeout=5, encoding='utf-8')
    #tnconn.logfile_read = sys.stdout
    #used to read all output of session; can also use logfile_write to view commands sent
    result = tnconn.expect([ssh_newkey, 'Password: ', pexpect.TIMEOUT])
    if result == 0:
        print('Accept SSH Fingerprint')
        tnconn.sendline('yes')
        result = tnconn.expect(['Password: ', pexpect.TIMEOUT])
        if result != 0:
            print('Failure Connecting to ' + IP)
            exit()
            tnconn.sendline(password)
    elif result == 1:
        tnconn.sendline(password)
    result = tnconn.expect(['>', '#', pexpect.TIMEOUT])
    if result == 0:
        tnconn.sendline('enable')
        result = tnconn.expect(['Password:', pexpect.TIMEOUT])
        if result != 0:
            print('Failure with enable command')
            exit()
        tnconn.sendline(password)
        result = tnconn.expect(['#', pexpect.TIMEOUT])
        if result != 0:
            print('Failure entering enable mode')
            exit()
    elif result == 1:
        pass
    elif result == 2:
        print('Failure with ' + IP)
        exit()
    tnconn.sendline('terminal length 0')
    result = tnconn.expect(['#', pexpect.TIMEOUT])
    if result != 0:
        print('Failure setting terminal length')
        exit()
    #tnconn.logfile_read = sys.stdout
    #prints output to screen
    output_file = open('running-config_for_{}_{}.txt'.format(IP, today), 'w')
    tnconn.logfile_read = output_file
    tnconn.sendline('show running-config')
    result = tnconn.expect(['#', pexpect.TIMEOUT])
    if result == 0:
        print('Successfully read running-config')
    elif result != 0:
        print('Command failure')
        exit()
    output_file.close()
    tnconn.close()

file.close()