import os
import time
import sys
import testinfra
import paramiko

def ssh_conn():
    client =



# establish remote connection
command = """sshpass -p '{}' ssh -o StrictHostKeyChecking=no {}@{} 'su - {} -c "{}"'""".format(
                ssh_passwd, ssh_user, hostname, user, cmd)

# zip file

target_dir="/usr/local/"
source = ['/home/swaroop/byte', '/home/swaroop/bin']
target = target_dir + time.strftime('%Y%m%d%H%M%S') + '.zip'
zip_command = "zip -qr '%s' %s" % (target, ' '.join(source))

if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('Backup FAILED')

