import time
import argparse
import pymysql
import os
import subprocess
from pyparsing import nestedExpr

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

# Returns:
# 1) testFileNameMapping: each input test to the list of split tests
# 2) testMapping: the filename of each test to the content of each test
def parseRTests():
    curString = ""
    status = 0 # not found anything yet
    testMapping = dict()
    testFileNameMapping = dict()
    for filename in os.listdir("AnomalyDetection/tests/testthat"):
        if filename.endswith(".R") and filename.startswith("test-"):
            testFilename = filename
            newTestFilenames = []
            with open(os.path.join("AnomalyDetection/tests/testthat/", filename)) as fp:
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

    return (testFileNameMapping, testMapping)

def functionToTestsLinking(functionName, testMapping):
    starterCode = "setwd(\"AnomalyDetection\")\nlibrary(devtools)\ndevtools::load_all(\".\")\n"
    
    startOfTestCode = "testFunc <- function() {\n"
    endOfTestCode = "\n}\n"
    startOfFunctionCall = "covr::function_coverage(\""
    endOfFunctionCall = "\", code = testFunc())\n"

    startOfIndividualTestCode = " <- function() {\n"
    endOfIndividualTestCode = "\n}\n"
    startOfIndividualFunctionCall = "covr::function_coverage(\""
    middleOfIndividualFunctionCall = "\", code = "
    endOfIndividualFunctionCall = "())\n"

    start = time.time()
    testNames = []
    open("devscript_covr_mapping.R", 'w').close()
    f = open("devscript_covr_mapping.R", "a")
    f.write(starterCode)
    end = time.time()

    print("Setup: ", end - start)
    functionIDs = dict()
    count = 0

    start = time.time()
    for testName in testMapping.keys():
        testNames.append(testName)
        testCode = testMapping[testName].strip()
        #print(testCode)
        testCode = testCode.split("\n")[1:]
        testCode.pop()
        testCode = "\n".join(testCode)
        testFunctionName = "testFunc_" + str(count) 
        f.write(testFunctionName)
        f.write(startOfIndividualTestCode)
        f.write(testCode)
        f.write(endOfIndividualTestCode)
        f.write(startOfIndividualFunctionCall)
        f.write(functionName)
        f.write(middleOfIndividualFunctionCall)
        f.write(testFunctionName)
        f.write(endOfIndividualFunctionCall)
        functionIDs[count] = testName
        count += 1
        #print(testCode)
        # full_rscript = starterCode + startOfTestCode + testCode + endOfTestCode + startOfFunctionCall + functionName + endOfFunctionCall
        # f = open("devscript_covr_mapping.R", "a")
        # f.write(full_rscript)
        # f.close()
        # subprocess.call("script mapping.txt")
        # subprocess.call("Rscript devscript_covr_mapping.R > mapping.txt 2>&1", shell = True)
        # subprocess.call("exit")
        #with open(os.path.join("mapping.txt")) as fp:
        #    line = fp.readline();
        #    link = False
        #    while line:
        #        if "Coverage:" in line:
        #            line = line.split("Coverage: ")[1].strip()[:-1]
        #            cov = float(line)
        #            print(str(cov))
        #        line = fp.readline();
            
    f.close()
    end = time.time()
    print("Write Test Code: ", end - start)
    
    start = time.time()
    subprocess.call("Rscript devscript_covr_mapping.R > mapping.txt 2>&1", shell = True)
    end = time.time()
    print("Script: ", end - start)
    count = 0
    testCases = []
    start = time.time()
    with open(os.path.join("mapping.txt")) as fp:
        line = fp.readline();
        link = False
        while line:
            if "Coverage:" in line:
                line = line.split("Coverage: ")[1].strip()[:-1]
                cov = float(line)
                # print(str(cov))
                if cov > 0:
                    testCases.append(functionIDs[count])
                # else:
                #    print("NO: ", functionIDs[count])
                count+=1
            line = fp.readline()
    end = time.time()
    print("Read File: ", end - start)

    return testCases
    
def testToSource(sourceToTestMapping):

    testToSource = dict()

    for source in sourceToTestMapping.keys():
        tests = sourceToTestMapping[source]
        for test in tests:
            if test in testToSource:
                testToSource[test].append(source)
            else:
                testToSource[test] = [source]

    return testToSource

def writeTestFile(functionNames, testMapping):
    starterCode = "setwd(\"AnomalyDetection\")\nlibrary(devtools)\ndevtools::load_all(\".\")\n"
    
    startOfTestCode = "testFunc <- function() {\n"
    endOfTestCode = "\n}\n"
    startOfFunctionCall = "covr::function_coverage(\""
    endOfFunctionCall = "\", code = testFunc())\n"

    startOfIndividualTestCode = " <- function() {\n"
    endOfIndividualTestCode = "\n}\n"
    startOfIndividualFunctionCall = "covr::function_coverage(\""
    middleOfIndividualFunctionCall = "\", code = "
    endOfIndividualFunctionCall = "())\n"

    start = time.time()

    start = time.time()
    testNames = []
    open("devscript_covr_mapping.R", 'w').close()
    f = open("devscript_covr_mapping.R", "a")
    f.write(starterCode)
    end = time.time()

    print("Setup: ", end - start)
    functionIDs = dict()
    count = 0

    for testName in testMapping.keys():
        testNames.append(testName)
        testCode = testMapping[testName].strip()
        #print(testCode)
        testCode = testCode.split("\n")[1:]
        testCode.pop()
        testCode = "\n".join(testCode)
        testFunctionName = "testFunc_" + str(count) 
        f.write(testFunctionName)
        f.write(startOfIndividualTestCode)
        f.write(testCode)
        f.write(endOfIndividualTestCode)
        functionIDs[count] = testName
        count += 1

    for i in range(0, count):
        for functionName in functionNames:
            testFunctionName = "testFunc_" + str(i) 
            f.write(startOfIndividualFunctionCall)
            f.write(functionName)
            f.write(middleOfIndividualFunctionCall)
            f.write(testFunctionName)
            f.write(endOfIndividualFunctionCall)

    return functionIDs

def processMappingFile(functionIDs, functionNames):
    numFunctions = len(functionNames)
    functionCount = 0
    testCount = 0
    testCase = ""
    testCases = []
    start = time.time()
    testToSourceMapping = dict()
    currentFunctions = []
    print(numFunctions)
    with open(os.path.join("mapping.txt")) as fp:
        line = fp.readline();
        link = False

        while line:
            if functionCount == numFunctions:
                testCase = functionIDs[testCount]
                print(testCase)
                testToSourceMapping[testCase] = currentFunctions
                currentFunctions = []
                functionCount = 0
                testCount += 1
            if "Coverage:" in line:
                line = line.split("Coverage: ")[1].strip()[:-1]
                cov = float(line)
                # print(str(cov))
                if cov > 0:
                    currentFunctions.append(functionNames[functionCount])
                    print(functionNames[functionCount])
                    # testCases.append(functionIDs[count])
                # else:
                #    print("NO: ", functionIDs[count])
                # print("Coverage!")
                functionCount+=1
            line = fp.readline()
    end = time.time()
    print("Read File: ", end - start)

    print(testToSourceMapping)

    return testToSourceMapping


def main():
    start = time.time()
    functions = getRFunctionList() # This returns a mapping of file names to functions
    functionNames = []
    for fileName in functions.keys():
        functionNames.extend(functions[fileName])
    functionNames = list(set(functionNames))
    testFileNameMapping, testMapping = parseRTests()
    #sourceToTest = dict()
    #for function in functionNames:
    #    print(function)
    #    sourceToTest[function] = functionToTestsLinking(function, testMapping)
        
    #testToSourceMapping = testToSource(sourceToTest)
    #print(testToSourceMapping)
    functionIDs = writeTestFile(functionNames, testMapping)
    start = time.time()
    subprocess.call("Rscript devscript_covr_mapping.R > mapping.txt 2>&1", shell = True)
    end = time.time()
    testToSourceMapping = processMappingFile(functionIDs, functionNames)
    print(testToSourceMapping)
    print("Elapsed: ", end - start)


if __name__ == "__main__":
    main()

