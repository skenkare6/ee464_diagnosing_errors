# Running the bash script wrapper.sh from this python script, and writing the output to a file
#!/usr/bin/python3

import subprocess

process = subprocess.call(['./wrapper.sh'])
#process.wait()

#for line in process.stdout.readlines():
#    print(line)
