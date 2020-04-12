# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors

subprocess.call('./wrapper.sh', shell=True)
print("\nConnecting to database...")
db = pymysql.connect(host = "localhost", database='test', user = "root", passwd = "S4ang4ai!")
cur = db.cursor()

functionList = []
testList = []
with open('changedFunctions.txt', 'r') as pr:
    #print("Functions that were changed:")
    for line in pr.readlines():
        line = line.strip()
        functionList.append(line)
        #print(line)
    pr.close()

with open('changedFunctions.txt', 'r') as fp:
    print("\nUsing function name, find function ID in database")
    print("Using function ID, find test ID that it maps to")
    print("Using test ID, find the test name in database\n")
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
        testList.append(result)
        #print(result)
    fp.close()
cur.close()
db.close()

s = "{"
for func in functionList:
    s = s + "'" + func + "',"
s = s[:-1]
s = s + "}"
print("The functions that have changed are: " + s)

t = "{"
for test in testList:
    t = t + "'" + test + "',"
t = t[:-1]
t = t + "}"
print("The tests to run are: " + t)
