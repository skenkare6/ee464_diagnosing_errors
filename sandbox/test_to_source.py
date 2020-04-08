import argparse
import pymysql
import os
import subprocess
from pyparsing import nestedExpr

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

    testNames = []
    open("devscript_covr_mapping.R", 'w').close()
    f = open("devscript_covr_mapping.R", "a")
    f.write(starterCode)
    functionIDs = dict()
    count = 0
    
    for testName in testMapping.keys():
        testNames.append(testName)
        print("Iteration")
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
    
    subprocess.call("Rscript devscript_covr_mapping.R > mapping.txt 2>&1", shell = True)
    count = 0
    testCases = []
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
                else:
                    print("NO: ", functionIDs[count])
                count+=1
            line = fp.readline()

    print(testCases)
            

def main():
    testFileNameMapping, testMapping = parseRTests()
    functionToTestsLinking("detect_anoms", testMapping)

if __name__ == "__main__":
    main()

