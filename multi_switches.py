import getpass
import pexpect

user = input('Enter your username: ')
password = getpass.getpass()


file = open('multi_switches.txt', mode = 'r')

for host in file:
    IP = host.strip()
    print('Configuring Switch ' + (IP))
    tnconn = pexpect.spawn('telnet ' + IP, timeout=5)
    result = tnconn.expect(['Username:', pexpect.TIMEOUT])
    if result != 0:
        print('Failure creating session for ' + IP)
        exit()
    tnconn.sendline(user)
    result = tnconn.expect(['Password:', pexpect.TIMEOUT])
    if result != 0:
        print('Failure logging into ' + IP)
        exit()
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
    tnconn.sendline('config terminal')
    result = tnconn.expect(['\(config\)#', pexpect.TIMEOUT])
    if result == 0:
        print('Entered config mode successfully')
    elif result != 0:
        print('Command failure')
        exit()
    hostname = 'hostname py_' + IP
    tnconn.sendline(hostname)
    result = tnconn.expect(['\(config\)#', pexpect.TIMEOUT])
    if result == 0:
        print('Entered command successfully')
    elif result != 0:
        print('Command failure')
        exit()
    tnconn.sendline('end')
    result = tnconn.expect(['#', pexpect.TIMEOUT])
    if result != 0:
        print('Command failure')
        exit()
    tnconn.sendline('copy running-config startup-config')
    result = tnconn.expect(['Destination filename \[startup-config\]?', pexpect.TIMEOUT])
    if result != 0:
        print('Command failure')
        exit()
    tnconn.sendline()
    #sendline () sends a blank line with a carriage return to confirm destination file name
    result = tnconn.expect(['#', pexpect.TIMEOUT])
    if result == 0:
        print('Save config successfully')
    elif result != 0:
        print('Command failure')
        exit()
    tnconn.close()

file.close()