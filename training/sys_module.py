import sys

print(sys.version)
sys.stderr.write('test\n')
sys.stderr.flush()
sys.stdout.write('this is stdout text\n')
print(dir(sys))

