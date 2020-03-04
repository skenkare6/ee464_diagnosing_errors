import sys, os, pytest, json

from Function import Function      # pylint: disable=import-error
from SourceFile import SourceFile  # pylint: disable=import-error
from Database import Database      # pylint: disable=import-error
from TestCase import TestCase      # pylint: disable=import-error

def test_get_by_name_test_case_exists(with_database):
  testCase = TestCase.get_by_name("first_test")
  assert set(testCase.functionsExercised) == set(["doMath"])
  assert set(testCase.filesExercised) == set(["one.r"])

def test_get_by_name_test_case_not_exists(with_database):
  testCase = TestCase.get_by_name("applesauce")
  assert testCase is None