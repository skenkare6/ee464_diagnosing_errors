# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors
import argparse
from pyparsing import nestedExpr
import time

db = pymysql.connect(host = "localhost", database = 'test', user = "root", passwd = "S4ang4ai!")

def testSelection():
    # get function names from git diff into changedCode.txt
    # check to see if repository is in database, if not, then exit (depends on when repository will be added)
    # parse changedFunctions.txt
    # go to database and find tests that match function names
    # output test names into JSON object
    cur = db.cursor()
    sql = ("SELECT path FROM Repositories;")
    cur.execute(sql);
    result = cur.fetchall()
    if not result:
        print("No repository has been added to the database. Please specify a database, or call redrawmappings, before moving forward.")
        exit(0)
    result = result[0][0]
    subprocess.call(['./getCodeChanges.sh testselection'+ ' ' + result], shell=True)

    functionList = dict()
    testList = dict()
    with open('changedCode.txt', 'r') as fp:
        funcs = set()
        for line in fp.readlines():
            line = line.strip()
            funcs.add(line)
        functionList['changedFunctions'] = funcs
        fp.close()

    with open('changedCode.txt', 'r') as fp:
        sql = ("SELECT * FROM RFunctions;")  # can we assume that if RFunction is populated than the other are as well?
        cur.execute(sql)
        r1 = cur.fetchall()
        if not r1:
            print("No mappings in the database, calling redrawmappings...")
            redrawMappings()
            exit(0)

        tests = set()
        for line in fp.readlines():
            line = line.strip()
            
            sql = ("SELECT functionID FROM RFunctions WHERE functionName = %s;")
            cur.execute(sql, (line))
            result = cur.fetchall()
            if not result:
                print("Function %s is not mapped in the database, calling redrawmappings..." % (line))
                redrawMappings()
                exit(0)
            result = result[0][0]

            sql = "SELECT testCaseID FROM RCodeToTestCases WHERE functionID = '%s';"
            cur.execute(sql, result)
            result = cur.fetchall()
            result = result[0][0]

            sql = "SELECT testCaseName FROM RTestCases WHERE testCaseID = '%s';"
            cur.execute(sql, result)
            result = cur.fetchall()
            result = result[0][0]
            tests.add(result)
        testList['testToRun'] = tests
        fp.close()
    cur.close()
    print(functionList)
    print(testList)    
    db.close()
    
def redrawMappings():
    # call DiffLinesFunction.sh
    # output file names into JSON object
    cur = db.cursor()

    sql = ("SELECT path FROM Repositories;")    # assuming that there will be at least one initial mapping before redrawmappings is called
    cur.execute(sql);
    result = cur.fetchall()
    result = result[0][0]
    if not result:
        print("No repository has been added to the database. Please specify a database before moving forward.")
        exit(0)

    fileList = dict()
    subprocess.call(['./getCodeChanges.sh redrawmappings'+ ' ' + result], shell=True)
    with open('changedCode.txt', 'r') as fp:
        files = set()
        for line in fp.readlines():
            lines = line.split()
            files.add(lines[0])
            #print(lines[0])
        fileList['filesToMap'] = files
        fp.close()
    print(fileList) # *** call test-to-source from here ***


def main():
    # 2 argument inputs that specify the 2 execution modes --mode redraw mappings or test selection
    # if redraw mappings, call diff lines function and get list of file names
    # if test selection, call wrapper.sh, and parse database, get list of test names
    parser = argparse.ArgumentParser(description='Pass arguments that specify test selection or redraw mapping.')
    parser.add_argument("-m", "--mode", help="execution mode to run (test selection or redraw mappings)")
    args = parser.parse_args()
    if((args.mode) is None):
        print("Please enter an execution mode to run (TESTSELECTION or REDRAWMAPPINGS)")
    else:        
        mode = (args.mode).lower()
        if(mode == "testselection"):
            testSelection()
        elif(mode == "redrawmappings"):
            redrawMappings()
        else:
            print("invalid argument")




if __name__ == "__main__":
    main()
