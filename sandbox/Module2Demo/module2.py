# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors

subprocess.call('./wrapper.sh', shell=True)
