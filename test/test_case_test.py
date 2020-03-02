import sys, os, pytest, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Function import Function
from SourceFile import SourceFile
from Database import Database
from TestCase import TestCase

def test_get_by_name_test_case_exists(with_database):
  testCase = TestCase.get_by_name("first_test")
  assert set(testCase.functionsExercised) == set(["doMath"])
  assert set(testCase.filesExercised) == set(["one.r"])

def test_get_by_name_test_case_not_exists(with_database):
  testCase = TestCase.get_by_name("applesauce")
  assert testCase is None