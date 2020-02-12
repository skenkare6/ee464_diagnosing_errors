import os
import subprocess
from pyparsing import nestedExpr

def getRFunctionList():
    subprocess.call("Rscript devscript_allFunctions.R > allFunctions.txt", shell = True)
    funcNames = []
    with open(os.path.join("allFunctions.txt")) as fp:
        line = fp.readline();
        while line:
            if ":" in line:
                split = line.split(':')[0]
                funcName = split.strip()
                # print(funcName)
                funcNames.append(funcName)
            line = fp.readline()
    return funcNames

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

    for func in mapping.keys():
        print(func + " called " + str(mapping[func]))
    return mapping

def parseRTests():
    curString = ""
    status = 0 # not found anything yet
    fullTests = []
    for filename in os.listdir("AnomalyDetection/tests/testthat"):
        if filename.endswith(".R") and filename.startswith("test-"):
            with open(os.path.join("AnomalyDetection/tests/testthat/", filename)) as fp:
            # content = fp.read()
            # print(content)
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
                        fullTests.append(curString)
                        curString = ""
                    line = fp.readline()
    # nestedExpr('(',')').parseString(content).asList()
    # print(nestedExpr)
    # for test in fullTests:
    #    print("TEST")
    #    print(test)
    return fullTests

def mapTestsToFunctions(mapping, tests):
    testMapping = dict()
    for test in tests:
        functions = set()
        for func in mapping.keys():
            if func in test:
                functions.add(func)
                functions.update(mapping[func])
        testMapping[test] = functions

    for test in testMapping.keys():
        print(test + " calls " + str(testMapping[test]))

def main():
    functions = getRFunctionList()
    mapping = getRFunctionCalls(functions)
    fullTests = parseRTests()
    mapTestsToFunctions(mapping, fullTests)

if __name__ == "__main__":
    main()

