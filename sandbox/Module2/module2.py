# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors
import argparse
from pyparsing import nestedExpr

db = pymysql.connect(host = "localhost", database = 'test', user = "root", passwd = "S4ang4ai!")

def testSelection():
    # call wrapper.sh
    # parse changedFunctions.txt
    # go to database and find tests that match function names
    # output test names into JSON object
    cur = db.cursor()
    subprocess.call('./getCodeChanges.sh testselection', shell=True)

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
        tests = set()
        for line in fp.readlines():
            line = line.strip()
            
            sql = ("SELECT functionID FROM RFunctions WHERE functionName = %s;")
            cur.execute(sql, (line))
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
    fileList = dict()
    subprocess.call('./getCodeChanges.sh redrawmappings', shell=True)
    with open('changedCode.txt', 'r') as fp:
        files = set()
        for line in fp.readlines():
            lines = line.split()
            files.add(lines[0])
            #print(lines[0])
        fileList['filesToMap'] = files
        fp.close()
    print(fileList)


def main():
    # 2 argument inputs that specify the 2 execution modes --mode redraw mappings or test selection
    # if redraw mappings, call diff lines function and get list of file names
    # if test selection, call wrapper.sh, and parse database, get list of test names
    parser = argparse.ArgumentParser(description='Pass arguments that specify test selection or redraw mapping.')
    parser.add_argument("-m", "--mode", help="execution mode to run (test selection or redraw mappings)")
    args = parser.parse_args()
    if((args.mode) is None):
        print("invalid argument")
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
