import time
import argparse
import pymysql
import os,sys
import subprocess
from pyparsing import nestedExpr
from Module2 import module2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/database_managers')))
from Repository import Repository
from Function import Function
from TestCase import TestCase
from SourceFile import SourceFile

def main():
    parser = argparse.ArgumentParser(description='Pass arguments in for the program to read the source code.')

    parser.add_argument("--doMappings", type=str, help="Regenerate mappings?")
    parser.add_argument("--testCaseName", type=str, help="R test case name")
    parser.add_argument("--repositoryPath", type=str, help="Repository Path")
    parser.add_argument("--harnessInput", type=str, help="Single File to Redo Mappings For")

    args = parser.parse_args()

    # Step 1: Module2 finds out which files have been changed
    subprocess.call("cd Module2 && python3 module2.py -r " + args.repositoryPath + " -m redrawMappings > ../newMappings.txt ", shell = True)

    # Step 2: Module1 updates mappings related to those files
    with open(os.path.join("newMappings.txt")) as fp:
        line = fp.readline();
        link = False

        while line:
            if line.startswith("R/"):
                line = line[2:]
                subprocess.call("python3 test_to_source.py --repositoryPath " + args.repositoryPath + " --harnessInput " + line, shell = True)

            line = fp.readline()

    # Step 3: Module2 outputs which tests need to be run
    subprocess.call("cd Module2 && python3 module2.py -r " + args.repositoryPath + " -m testSelection ", shell = True)

if __name__ == "__main__":
    main()

