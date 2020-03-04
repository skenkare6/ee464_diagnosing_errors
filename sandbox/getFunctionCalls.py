import argparse
import pymysql
import os
import subprocess
from pyparsing import nestedExpr

# For now, pull in the ORM classes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/database_managers')))
from Repository import Repository

con = pymysql.connect('localhost', 'newuser', 'password', 'ee464_test_db')

def getRFunctionList():
    subprocess.call("Rscript devscript_allFunctions.R > allFunctions.txt", shell = True)
    mapping = dict()
    with open(os.path.join("allFunctions.txt")) as fp:
        line = fp.readline();
        fileName = ""
        funcs = []
        while line:
            if "FILE: " in line:
                if fileName:
                    mapping[fileName] = funcs
                split = line.split(':')[1]
                fileName = split.strip()
                funcs = []
            elif ":" in line:
                split = line.split(':')[0]
                funcName = split.strip()
                # print(funcName)
                funcs.append(funcName)
            line = fp.readline()

    mapping[fileName] = funcs

    return mapping

def getRFunctionCalls(functions):
    open("getFunctionCalls.txt", 'w').close()
    for function in functions:
        # print("Function: " + function)
        subprocess.call("Rscript devscript_callGraph.R " + function + " >> getFunctionCalls.txt", shell = True)

    mapping = dict()
    with open(os.path.join("getFunctionCalls.txt")) as fp:
        line = fp.readline()
        count = 0 # each '0' line is the name of the function, each '1' line is all the functions called by it
        curName = line
        while line:
            if count == 0:
                curName = line.strip()
            else:
                called = line.split(' ')
                filtered = []
                for func in called:
                    if func in functions:
                        filtered.append(func)
                mapping[curName] = filtered
            count ^= 1
            line = fp.readline()

    #for func in mapping.keys():
        #print(func + " called " + str(mapping[func]))
    return mapping

def parseRTests():
    curString = ""
    status = 0 # not found anything yet
    # fullTests = []
    testMapping = dict()
    testFileNameMapping = dict()
    for filename in os.listdir("AnomalyDetection/tests/testthat"):
        if filename.endswith(".R") and filename.startswith("test-"):
            testFilename = filename
            newTestFilenames = []
            with open(os.path.join("AnomalyDetection/tests/testthat/", filename)) as fp:
            # content = fp.read()
            # print(content)
                count = 0
                line = fp.readline()
                while line:
                # print(line)
                    if "test_that" in line:
                        status = 1
                        curString += line
                    elif status == 1:
                        curString += line
                    if curString.count('(') == curString.count(')') and status == 1:
                        status = 0
                        #fullTests.append(curString)
                        newTestFilename = filename[:-2] + "-" + str(count) + ".R"
                        newTestFilenames.append(newTestFilename)
                        text_file = open(newTestFilename, "w")
                        text_file.write(curString)
                        text_file.close()
                        testMapping[newTestFilename] = curString
                        curString = ""
                        count += 1
                    line = fp.readline()
            testFileNameMapping[testFilename] = newTestFilenames
    # nestedExpr('(',')').parseString(content).asList()
    # print(nestedExpr)
    # for test in fullTests:
    #    print("TEST")
    #    print(test)
    # return fullTests
    src = "AnomalyDetection"
    rCode = "AnomalyDetection"
    with con:
        cur = con.cursor()
        # Add codebase to repos table
        selectSql = "SELECT repositoryID FROM `Repositories` WHERE path = %s"
        cur.execute(selectSql, (src))
        results = cur.fetchall()
        if not results:
            sql = "INSERT INTO `Repositories` (`path`) VALUES (%s)"
            con.cursor().execute(sql, (src))

        cur.execute(selectSql, (src))
        repoID = cur.fetchall()[0][0]
        # print(repoID)

        # Add files to files table
        for f in testFileNameMapping.keys():
            p = os.path.join(rCode, f)
            selectSql = "SELECT fileID FROM `RFiles` WHERE filePath = %s"
            cur.execute(selectSql, (p))
            results = cur.fetchall()
            if not results:
                # print("No results!")
                sql = "INSERT INTO `RFiles` (`repositoryID`, `filePath`, `fileType`) VALUES (%s, %s, %s)"
                con.cursor().execute(sql, (repoID, p, str(1)))

            funcs = testFileNameMapping[f]
            # print(f)
            # print(funcs)
            cur.execute(selectSql, (p))
            fileID = cur.fetchall()[0][0]
            # print(fileID)
            for func in funcs:
                selectSql = "SELECT testCaseID FROM `RTestCases` WHERE testCaseName = %s and fileID = %s"
                cur.execute(selectSql, (func,str(fileID),))
                results = cur.fetchall()
                if not results:
                    sql = "INSERT INTO `RTestCases` (`fileID`, `testCaseName`) VALUES (%s, %s)"
                    con.cursor().execute(sql, (str(fileID), func))

    return testMapping

def mapTestsToFunctions(mapping, tests):
    testMapping = dict()
    for test in tests.keys():
        functions = set()
        for func in mapping.keys():
            if func in tests[test]:
                functions.add(func)
                functions.update(mapping[func])
        testMapping[test] = functions

    for test in testMapping.keys():
        print(test + " calls " + str(testMapping[test]))

    for test in testMapping.keys():
        for func in testMapping[test]:
            with con:
                cur = con.cursor()
                selectSql = "SELECT functionID FROM `RFunctions` WHERE functionName = %s"
                cur.execute(selectSql, func)
                results = cur.fetchall()
                functionID = results[0][0]

                selectSql = "SELECT testCaseID FROM `RTestCases` WHERE testCaseName = %s"
                cur.execute(selectSql, test)
                results = cur.fetchall()
                testCaseID = results[0][0]

                selectSql = "SELECT * FROM `RCodeToTestCases` WHERE `functionID` = %s AND testCaseID = %s"
                cur.execute(selectSql, (str(functionID), str(testCaseID)))
                results = cur.fetchall()

                if not results:
                    sql = "INSERT INTO `RCodeToTestCases` (`functionID`, `testCaseID`) VALUES (%s, %s)"
                    con.cursor().execute(sql, (str(functionID), str(testCaseID)))

    return testMapping

def storeFilesAndFunctions(mapping):
    src = "AnomalyDetection"
    rCode = "AnomalyDetection"

    repo = Repository.get_by_path(src)
    repo = Repository.create(src) if not repo else repo

    # Add files to files table
    for f in mapping.keys():
        filePath = os.path.join(rCode, f)

        file = SourceFile.get_by_file_path(filePath)
        file = SourceFile.create(filePath, 0, repo.repoID) if not file else file

        for func in mapping[f]:
            function = Function.get_by_name_and_file_id(func, file.fileID)
            if not function:
              Function.create(file.fileID, func)

def searchInDatabase(testFile):
    print()

    with con:
        cur = con.cursor()
        sql = "SELECT functionName from RFunctions where RFunctions.functionID in (SELECT RCodeToTestCases.functionID from RCodeToTestCases where testCaseID in (select testCaseID from RTestCases where testCaseName=%s))"
        cur.execute(sql, (testFile))
        functions = cur.fetchall()
        for func in functions:
            print(func[0])

def main():
    parser = argparse.ArgumentParser(description='Pass arguments in for the program to read the source code.')

    parser.add_argument("--doMappings", type=str, help="Regenerate mappings?")
    parser.add_argument("--testFile", type=str, help="R test file")

    args = parser.parse_args()
    if args.doMappings and args.doMappings == "true":
        functions = getRFunctionList() # This returns a mapping of file names to functions
        storeFilesAndFunctions(functions)
        functionNames = []
        for fileName in functions.keys():
            functionNames.extend(functions[fileName])
        functionNames = list(set(functionNames))
        mapping = getRFunctionCalls(functionNames)
        fullTests = parseRTests()
        testMapping = mapTestsToFunctions(mapping, fullTests)
        if args.testFile:
            print(testMapping[args.testFile])

    if args.doMappings and args.doMappings == "false" and args.testFile:
        searchInDatabase(args.testFile)




if __name__ == "__main__":
    main()

