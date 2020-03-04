import sys, os, pytest, json

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

def test_create(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.create("someTest", file.fileID)

  assert testCase is not None
  assert testCase.name == "someTest"