import os
import pymysql.cursors

db = pymysql.connect(
        host = "localhost",
        database = 'test',
        user = "root",
        passwd = "S4ang4ai!" # your password
)

directory = os.getcwd();
cur = db.cursor()
cur.execute("INSERT INTO Repositories(path) VALUES ('AnomalyDetection');")
db.commit()
cur.execute("SELECT repositoryID FROM Repositories WHERE path = 'AnomalyDetection';")
results = cur.fetchall()
repID = results[0][0]

insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'tests/testthat/test-NAs.R', 2);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'tests/testthat/test-edge.R', 2);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'tests/testthat/test-ts.R', 2);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'tests/testthat/test-vec.R', 2);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'R/date_utils.R', 1);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'R/detect_anoms.R', 1);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'R/plot_utils.R', 1);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'R/raw_data.R', 1);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'R/ts_anom_detection.R', 1);"
cur.execute(insert, str(repID))
db.commit()
insert = "INSERT INTO RFiles(repositoryID, filePath, fileType) VALUES (%s, 'R/vec_anom_detection.R', 1);"
cur.execute(insert, str(repID))
db.commit()

cur.execute("SELECT fileID FROM RFiles WHERE filePath = 'R/ts_anom_detection.R';")
results = cur.fetchall()
fID = results[0][0]
insert = "INSERT INTO RFunctions(fileID, functionName) VALUES (%s, 'AnomalyDetectionTs');"
cur.execute(insert, str(fID))
db.commit()
cur.execute("SELECT fileID FROM RFiles WHERE filePath = 'R/vec_anom_detection.R';")
db.commit()
results = cur.fetchall()
fID = results[0][0]
insert = "INSERT INTO RFunctions(fileID, functionName) VALUES (%s, 'AnomalyDetectionVec');"
cur.execute(insert, str(fID))
db.commit()

cur.execute("SELECT fileID FROM RFiles WHERE filePath = 'tests/testthat/test-ts.R';")
db.commit()
results = cur.fetchall()
tId = results[0][0]
insert = "INSERT INTO RTestCases(fileID, testCaseName) VALUES (%s, 'test-ts.R');"
cur.execute(insert, tId)
db.commit()
cur.execute("SELECT fileID FROM RFiles WHERE filePath = 'tests/testthat/test-vec.R';")
db.commit()
results = cur.fetchall()
tId = results[0][0]
insert = "INSERT INTO RTestCases(fileID, testCaseName) VALUES (%s, 'test-vec.R');"
cur.execute(insert, tId)
db.commit()
#cur.execute("INSERT INTO RTestCases(fileID, testName) VALUES (%s, 'test-edge.R');")
#cur.execute("INSERT INTO RTestCases(fileID, testName) VALUES (%s, 'test-NAs.R');")

cur.execute("SELECT functionID FROM RFunctions WHERE functionName = 'AnomalyDetectionTs';")
db.commit()
funcInsert = cur.fetchall()
funcID = funcInsert[0][0]
cur.execute("SELECT testCaseID FROM RTestCases WHERE testCaseName = 'test-ts.R';")
db.commit()
testInsert = cur.fetchall()
testID = testInsert[0][0]

insert = "INSERT INTO RCodeToTestCases(functionID, testCaseID) VALUES (%s, %s);"
cur.execute(insert, (str(funcID), str(testID)))
db.commit()

cur.execute("SELECT functionID FROM RFunctions WHERE functionName = 'AnomalyDetectionVec';")
db.commit()
funcInsert = cur.fetchall()
funcID = funcInsert[0][0]
cur.execute("SELECT testCaseID FROM RTestCases WHERE testCaseName = 'test-vec.R';")
db.commit()
testInsert = cur.fetchall()
testID = testInsert[0][0]

insert = "INSERT INTO RCodeToTestCases(functionID, testCaseID) VALUES (%s, %s);"
cur.execute(insert, (str(funcID), str(testID)))
db.commit()

cur.close()
db.close()
