import argparse
import pymysql
import os, sys
import subprocess
import timeit
import time
import glob
from subprocess import Popen, PIPE, STDOUT
from statistics import mean 
from pyparsing import nestedExpr

do_mapping_error="******* No correct flag specified, please use true or false next time *******"
test_case_name_error="********* Test case was not found *********"
empty_test_case_error="test_to_source.py: error: argument --doMappings: expected one argument"
addition_output='{\\n "test-addition-0.R": {\\n  "functions": [\\n   "add2nums"\\n  ],\\n  "files": [\\n   "workwork/R/add2nums.R"\\n  ]\\n }\\n}'
sub_output='{\\n "test-subtraction-0.R": {\\n  "functions": [\\n   "sub2nums"\\n  ],\\n  "files": [\\n   "workwork/R/sub2nums.R"\\n  ]\\n }\\n}'
mult_output='{\\n "test-multiply-0.R": {\\n  "functions": [\\n   "mult2nums"\\n  ],\\n  "files": [\\n   "workwork/R/mult2nums.R"\\n  ]\\n }\\n}'
div_output='{\\n "test-divs-0.R": {\\n  "functions": [\\n   "div2nums"\\n  ],\\n  "files": [\\n   "workwork/R/div2nums.R"\\n  ]\\n }\\n}'
all_output='{\\n "test-all-0.R": {\\n  "functions": [\\n   "mult2nums",\\n   "div2nums",\\n   "sub2nums",\\n   "add2nums"\\n  ],\\n  "files": [\\n   "workwork/R/mult2nums.R",\\n   "workwork/R/div2nums.R",\\n   "workwork/R/sub2nums.R",\\n   "workwork/R/add2nums.R"\\n  ]\\n }\\n}'



def mappings():
	print("test")

def h_function():
	cmd = 'python3 test_to_source.py -h'
	p = Popen(cmd, shell=True,  stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert (output[0:5]=='usage')

def help_function():
	cmd = 'python3 test_to_source.py --help'
	p = Popen(cmd, shell=True,  stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert (output[0:5]=='usage')

def inval_do_mapping():
	cmd = 'python3 test_to_source.py --doMappings asdf'
	p = Popen(cmd, shell=True,  stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==do_mapping_error


def inval_test_case():
	cmd = 'python3 test_to_source.py --doMappings false --testCaseName asdf'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==test_case_name_error

def do_mapping_true():
	cmd= 'python3 test_to_source.py --doMappings true --testCaseName test-addition-0.R --repositoryPath workwork' 
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:7]
	assert output=='Setup'

def check_add_map():
	cmd= 'python3 test_to_source.py --doMappings false --testCaseName test-addition-0.R --repositoryPath workwork' 
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==addition_output

def check_sub_map():
	cmd= 'python3 test_to_source.py --doMappings false --testCaseName test-subtraction-0.R --repositoryPath workwork' 
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==sub_output

def check_mult_map():
	cmd= 'python3 test_to_source.py --doMappings false --testCaseName test-multiply-0.R --repositoryPath workwork' 
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==mult_output


def check_div_map():
	cmd= 'python3 test_to_source.py --doMappings false --testCaseName test-divs-0.R --repositoryPath workwork' 
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==div_output


def check_all_map():
	cmd= 'python3 test_to_source.py --doMappings false --testCaseName test-all-0.R --repositoryPath workwork' 
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
	output = p.stdout.read()
	output = str(output)[2:-3]
	assert output==all_output

def main():
	h_function()
	help_function()
	inval_do_mapping()
	inval_test_case()
	do_mapping_true()
	check_add_map()
	check_sub_map()
	check_mult_map()
	check_div_map()
	check_all_map()
	print("All passed")
	

if __name__=="__main__":
	main()
