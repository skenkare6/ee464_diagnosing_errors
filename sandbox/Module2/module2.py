# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors
import argparse
from pyparsing import nestedExpr
import time

db = pymysql.connect(host = "localhost", database = 'test', user = "root", passwd = "S4ang4ai!")

def testSelection(repo):
    # get function names from git diff into changedCode.txt
    # check to see if repository is in database, if not, then exit (depends on when repository will be added)
    # parse changedFunctions.txt
    # go to database and find tests that match function names
    # output test names into JSON object
    cur = db.cursor()
    sql = ("SELECT path FROM Repositories WHERE path = %s;")
    cur.execute(sql, repo);
    result = cur.fetchall()
    if not result:
        print("Incorrect repository name. Please specify a correct repository name, or add %s to the database." % repo)
        return;
    subprocess.call(['./getCodeChanges.sh testselection'+ ' ' + repo], shell=True)

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
            return;

        tests = set()
        for line in fp.readlines():
            line = line.strip()
            
            sql = ("SELECT functionID FROM RFunctions WHERE functionName = %s;")
            cur.execute(sql, (line))
            result = cur.fetchall()
            if not result:
                print("Function %s is not mapped in the database, calling redrawmappings..." % (line))
                redrawMappings()
                return;
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
    
def redrawMappings(repo):
    # call DiffLinesFunction.sh
    # output file names into JSON object
    cur = db.cursor()
    
    sql = ("SELECT path FROM Repositories WHERE path = %s;")
    cur.execute(sql, repo)
    result = cur.fetchall()
    if not result:
        print("Incorrect repository name. Please specify a correct repository name, or add %s to the database." % repo)
        return

    fileList = dict()
    subprocess.call(['./getCodeChanges.sh redrawmappings'+ ' ' + repo], shell=True)
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
    # 2 argument inputs that specify the execution mode (--mode testselection or redrawmappings) and  
    #   the repository name 
    # if mode == redraw mappings, call diff lines function and get list of file names
    # if mode == test selection, call wrapper.sh, and parse database, get list of test names
    parser = argparse.ArgumentParser(description='Pass arguments that specify the repository name and execution mode.')
    parser.add_argument("-m", "--mode", help="execution mode to run (testselection or redrawmappings)")
    parser.add_argument("-r", "--repoName", help="the name of the github repository")
    args = parser.parse_args()
    if((args.repoName) is None):
        print("Please enter the name of the repository")
    else:
        if((args.mode) is None):
            print("Please enter an execution mode to run (TESTSELECTION or REDRAWMAPPINGS)")
        else:        
            mode = (args.mode).lower()
            if(mode == "testselection"):
                testSelection(repo = args.repoName)
            elif(mode == "redrawmappings"):
                redrawMappings(repo = args.repoName)
            else:
                print("invalid argument")




if __name__ == "__main__":
    main()
