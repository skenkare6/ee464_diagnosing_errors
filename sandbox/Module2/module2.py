# Running the bash script wrapper.sh from this python script, and writing the output to a file
import subprocess
from subprocess import Popen
import pymysql.cursors
import argparse
from pyparsing import nestedExpr
import time
import sys, os

# For now, pull in the ORM classes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/database_managers')))
from Repository import Repository
from Function import Function

def testSelection(repo):
    # get function names from git diff into changedCode.txt
    # check to see if repository is in database, if not, then exit (depends on when repository will be added)
    # parse changedFunctions.txt
    # go to database and find tests that match function names
    # output test names into JSON object
    result = Repository.get_by_path(repo)

    if not result:
        print("No repository has been added to the database. Please specify a database, or call redrawmappings, before moving forward.")
        exit(1)

    subprocess.call(['./getCodeChanges.sh testselection'+ ' ' + result.path], shell=True)

    functionList = dict()
    testList = dict()
    with open('changedCode.txt', 'r') as fp:
        funcs = set()
        for line in fp.readlines():
            line = line.strip()
            funcs.add(line)
        functionList['changedFunctions'] = funcs

    with open('changedCode.txt', 'r') as fp:
        functions = Function.get_all()

        if not functions or len(functions) == 0:
            print("No mappings in the database, calling redrawmappings...")
            redrawMappings()
            exit(1)

        tests = list()
        for functionName in fp.readlines():
            functionName = functionName.strip()
            function = Function.get_by_name(functionName)

            if not function:
                print("Function %s is not mapped in the database, calling redrawmappings..." % (functionName))
                redrawMappings()
                exit(1)

            tests.extend(function.testCaseNames)
        testList['testToRun'] = set(tests)

    print(functionList)
    print(testList)

def redrawMappings(repo):
    # call DiffLinesFunction.sh
    # output file names into JSON object
    repo = Repository.get_by_path(repo)

    if not repo:
        print("No repository has been added to the database. Please specify a database before moving forward.")
        exit(1)

    fileList = dict()
    subprocess.call(['./getCodeChanges.sh redrawmappings'+ ' ' + repo.path], shell=True)

    # print(testList)

    with open('changedCode.txt', 'r') as fp:
        files = set()
        for line in fp.readlines():
            lines = line.split()
            files.add(lines[0])
            #print(lines[0])
        fileList['filesToMap'] = files
        fp.close()

    # print(fileList) # *** call test-to-source from here ***
    for f in fileList['filesToMap']:
        print(f)


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
