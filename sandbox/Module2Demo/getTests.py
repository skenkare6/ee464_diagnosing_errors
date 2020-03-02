import pymysql.cursors

db = pymysql.connect(host = "localhost", database='test', user = "root", passwd = "S4ang4ai!")
cur = db.cursor()

with open('changedFunctions.txt', 'r') as fp:
    for line in fp.readlines():
        line = line.strip()
        #print("Changed function: "+ line)
        #sql = "SELECT functionID FROM RFunctions WHERE functionName = '%s';"
        #sql = "SELECT * FROM RFunctions;"
        #cur.execute(sql, line)
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
