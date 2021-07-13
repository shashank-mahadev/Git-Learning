import argparse
from datetime import datetime




now = datetime.now()
current_time = now.strftime("%y%M%D")


parser = argparse.ArgumentParser()
parser.add_argument('--start_date', help='provide the current time', default=current_time)
parser.add_argument('--host_name', help='server name')
parser.add_argument('--iterat', help='type number of iteration', type=int, default=4)






import os
import time


#print(dir(os))

old_dir = ['/Users/unraveldata/test/shashank.txt', '/Users/unraveldata/test/shank.txt', '/Users/unraveldata/test/chantan.txt', '/Users/unraveldata/test/chetan.txt']
new_dir = '/Users/unraveldata/test1'
# pwd=os.listdir(".")
# print(pwd)
target = new_dir + current_time + '.zip'
zip_cmd = "zip -qr '%s' %s" % (target, ''.join(old_dir))
#tar = 'tar -cvzf %s %s -X /home/swaroop/excludes.txt' % (target, ' '.join(old_dir))
print(zip_cmd)
if os.system(zip_cmd) == 0:
    print('success')
else:
    print('fail')