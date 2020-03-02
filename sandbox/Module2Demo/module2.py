# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors

subprocess.call('./wrapper.sh', shell=True)
db = pymysql.connect(host = "localhost", database='test', user = "root", passwd = "S4ang4ai!")
cur = db.cursor()

with open('changedFunctions.txt', 'r') as pr:
    print("Functions that were changed:")
    for line in pr.readlines():
        line = line.strip()
        print(line)
    pr.close()

with open('changedFunctions.txt', 'r') as fp:
    print("\nTests to be run:")
    for line in fp.readlines():
        line = line.strip()
        
        cur.execute("SELECT functionID FROM RFunctions WHERE functionName = 'AnomalyDetectionTs';")
        result = cur.fetchall()
        result = result[0][0]

        sql = "SELECT testCaseID FROM RCodeToTestCases WHERE functionID = '%s';"
        cur.execute(sql, result)
        result = cur.fetchall()
        result = result[0][0]

        sql = "SELECT testCaseName FROM RTestCases WHERE testCaseID = '%s';"
        cur.execute(sql, result)
        result = cur.fetchall()
        result = result[0][0]
        print(result)
    fp.close()
cur.close()
db.close()
