import time
import argparse
import pymysql
import os,sys
import subprocess
from pyparsing import nestedExpr

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/database_managers')))
from Repository import Repository
from Function import Function
from TestCase import TestCase
from SourceFile import SourceFile

def getRFunctionList(src):
    src = src + "/R"
    subprocess.call("Rscript devscript_allFunctions.R " + src + "> allFunctions.txt", shell = True)
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

def getFunctionListForFile(src, fileName):
    src = src + "/R"
    subprocess.call("Rscript devscript_functionsInFile.R " + src + " " + fileName + " > allFunctions.txt", shell = True)
    mapping = dict()
    with open(os.path.join("allFunctions.txt")) as fp:
        line = fp.readline();
        funcs = []
        while line:
            if ":" in line:
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
def parseRTests(src):
    curString = ""
    status = 0 # not found anything yet
    testMapping = dict()
    testFileNameMapping = dict()
    for filename in os.listdir(src + "/tests/testthat"):
        if filename.endswith(".R") and filename.startswith("test-"):
            testFilename = filename
            newTestFilenames = []
            with open(os.path.join(src + "/tests/testthat/", filename)) as fp:
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
    
    rCode = src + "/tests/testthat"
    repo = Repository.get_by_path(src)
    repo = Repository.create(src) if not repo else repo

    # Add files to files table
    for f in testFileNameMapping.keys():
        filePath = os.path.join(rCode, f)

        if len(f) > 0:
          file = SourceFile.get_by_file_path(filePath)

          if not file:
            file = SourceFile.create(filePath, 1, repo.path)

          funcs = testFileNameMapping[f]

          testCase = TestCase.get_by_name_and_file_id(f, file.fileID)

          if not testCase:
            testCase = TestCase.create(f, file.fileID)
          
          for func in funcs:
            testCase = TestCase.get_by_name_and_file_id(func, file.fileID)

            if not testCase:
              testCase = TestCase.create(func, file.fileID)

    return (testFileNameMapping, testMapping)

def functionToTestsLinking(src, functionName, testMapping):
    starterCode = "setwd(\"" + src + "\")\nlibrary(devtools)\ndevtools::load_all(\".\")\n"
    
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

def writeTestFile(src, functionNames, testMapping):
    starterCode = "setwd(\"" + src + "\")\nlibrary(devtools)\ndevtools::load_all(\".\")\n"
    
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
    print(functionNames)
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
                # print(testCase)
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
                    # print(functionNames[functionCount])
                    # testCases.append(functionIDs[count])
                # else:
                #    print("NO: ", functionIDs[count])
                # print("Coverage!")
                functionCount+=1
            line = fp.readline()
    end = time.time()
    # print("Read File: ", end - start)

    # print(testToSourceMapping)

    return testToSourceMapping

def storeMappingInDatabase(testToSourceMapping):
    for test in testToSourceMapping.keys():
        testCase = TestCase.get_by_name(test)
        for func in testToSourceMapping[test]:
            function = Function.get_by_name(func)
            mapping = testCase.get_mapping(function)

            if not mapping:
              testCase.create_mapping(function)

            # testCase.create_mapping(function)

def mapOriginalTests(testFileNameMapping, testToSourceMapping):
    # print(testFileNameMapping)
    fullTestToSourceMapping = dict()
    for test in testToSourceMapping.keys():
        fullTestToSourceMapping[test] = testToSourceMapping[test]

    for test in testToSourceMapping.keys():
        for bigTest in testFileNameMapping.keys():
            if test in testFileNameMapping[bigTest]:
                fullTestToSourceMapping[bigTest] = testToSourceMapping[test]

    return fullTestToSourceMapping

def searchInDatabase(testCaseName):
  tc=TestCase.get_by_name(testCaseName)
  if tc is None:
    print("********* Test case was not found *********")
  else:
    print(TestCase.get_by_name(testCaseName).to_json())

def storeFilesAndFunctions(src, mapping):
    rCode = src + "/R"

    repo = Repository.get_by_path(src)
    repo = Repository.create(src) if not repo else repo

    # Add files to files table
    for f in mapping.keys():
        filePath = os.path.join(rCode, f)

        if len(f) > 0:
          file = SourceFile.get_by_file_path(filePath)

          if file is None:
            file = SourceFile.create(filePath, 1, repo.path)

          for func in mapping[f]:
            function = Function.get_by_name_and_file_id(func, file.fileID)
            if not function:
              Function.create(func, file.fileID)

def main():
    parser = argparse.ArgumentParser(description='Pass arguments in for the program to read the source code.')

    parser.add_argument("--doMappings", type=str, help="Regenerate mappings?")
    parser.add_argument("--testCaseName", type=str, help="R test case name")
    parser.add_argument("--repositoryPath", type=str, help="Repository Path")
    parser.add_argument("--harnessInput", type=str, help="Single File to Redo Mappings For")

    args = parser.parse_args()
    if args.harnessInput:
        fileName = args.harnessInput
        functions = getFunctionListForFile(args.repositoryPath, fileName)
        functionNames = []
        for fileName in functions.keys():
            functionNames.extend(functions[fileName])
        functionNames = list(set(functionNames))
        #print(functionNames)
        testFileNameMapping, testMapping = parseRTests(args.repositoryPath)
        functionIDs = writeTestFile(args.repositoryPath, functionNames, testMapping)
        #print(functionIDs)
        subprocess.call("Rscript devscript_covr_mapping.R > mapping.txt 2>&1", shell = True)
        testToSourceMapping = processMappingFile(functionIDs, functionNames)
        testToSourceMapping = mapOriginalTests(testFileNameMapping, testToSourceMapping)
        print(testToSourceMapping)
        storeMappingInDatabase(testToSourceMapping)

    if args.doMappings and args.doMappings == "true":
        start = time.time()
        functions = getRFunctionList(args.repositoryPath) # This returns a mapping of file names to functions
        storeFilesAndFunctions(args.repositoryPath, functions)
        functionNames = []
        for fileName in functions.keys():
            functionNames.extend(functions[fileName])
        functionNames = list(set(functionNames))
        testFileNameMapping, testMapping = parseRTests(args.repositoryPath)
        functionIDs = writeTestFile(args.repositoryPath, functionNames, testMapping)
        #start = time.time()
        subprocess.call("Rscript devscript_covr_mapping.R > mapping.txt 2>&1", shell = True)
        #end = time.time()
        testToSourceMapping = processMappingFile(functionIDs, functionNames)
        testToSourceMapping = mapOriginalTests(testFileNameMapping, testToSourceMapping)
        #print(testToSourceMapping)
        storeMappingInDatabase(testToSourceMapping)
        #print("Elapsed: ", end - start)

    if args.doMappings and args.doMappings == "false" and args.testCaseName:
        searchInDatabase(args.testCaseName)

    if not(args.doMappings == "false" or args.doMappings=="true"):
        print("******* No correct flag specified, please use true or false next time *******")


if __name__ == "__main__":
    main()

