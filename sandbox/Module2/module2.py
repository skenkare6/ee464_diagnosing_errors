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

def testSelection():
    # get function names from git diff into changedCode.txt
    # check to see if repository is in database, if not, then exit (depends on when repository will be added)
    # parse changedFunctions.txt
    # go to database and find tests that match function names
    # output test names into JSON object
    result = Repository.get_all()

    if not result or len(result) == 0:
        print("No repository has been added to the database. Please specify a database, or call redrawmappings, before moving forward.")
        exit(1)

    result = result[0]
#    print(result.path)
#    print(Repository.get_all())
#    a = input("press a")

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

        tests = set()
        for functionName in fp.readlines():
            functionName = functionName.strip()
            function = Function.get_by_name(functionName)

            if not function:
                print("Function %s is not mapped in the database, calling redrawmappings..." % (functionName))
                redrawMappings()
                exit(1)

            tests.add(function.testCaseNames)

        testList['testToRun'] = tests

    print(functionList)
    print(testList)

def redrawMappings():
    # call DiffLinesFunction.sh
    # output file names into JSON object
    repos = Repository.get_all()

    if not repos or len(repos) == 0:
        print("No repository has been added to the database. Please specify a database before moving forward.")
        exit(1)

    targetRepo = repos[0]

    fileList = dict()
    subprocess.call(['./getCodeChanges.sh redrawmappings'+ ' ' + targetRepo.path], shell=True)

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
