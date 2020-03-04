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

def test_get_by_name_and_file_id_exists(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.get_by_name_and_file_id("first_test", file.fileID)

  assert testCase is not None
  assert testCase.name == "first_test"
  assert file.fileID in testCase.fileIdsExercised

def test_get_by_name_and_file_id_not_exists(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.get_by_name_and_file_id("apoiwjdaiopwhd", file.fileID)

  assert testCase is None

def test_create_mapping_between_test_and_function(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.create("apoijwdapoijwd", file.fileID)
  function = Function.create("paoiwdjaowidj", file.fileID)

  testCase.create_mapping(function)
  function = Function.get_by_name_and_file_id(function.name, file.fileID)

  assert testCase.name in function.testCaseNames

def test_delete_mapping_between_test_and_function(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.create("apoijwdapoijwd", file.fileID)
  function = Function.create("paoiwdjaowidj", file.fileID)

  testCase.create_mapping(function)
  testCase.delete_mapping(function)
  function = Function.get_by_name_and_file_id(function.name, file.fileID)

  assert testCase.name not in function.testCaseNames

def test_create(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.create("someTest", file.fileID)

  assert testCase is not None
  assert testCase.name == "someTest"

def test_assigns_all_fields_with_mappings(with_database):
  file = SourceFile.get_by_file_path("one.r")
  testCase = TestCase.create("apoijwdapoijwd", file.fileID)
  function = Function.create("paoiwdjaowidj", file.fileID)

  testCase.create_mapping(function)

  assert testCase.filesExercised is not None
  assert testCase.functionsExercised is not None
  assert testCase.fileIdsExercised is not None
  assert testCase.testCaseID is not None
  assert testCase.name is not None

def test_assigns_all_fields_but_exercised_with_mappings(with_database):
  file = SourceFile.create("blah.r", 0, ".")
  testCase = TestCase.create("apoijwdapoijwd", file.fileID)

  assert testCase.filesExercised is None or len(testCase.filesExercised) == 0
  assert testCase.functionsExercised is None or len(testCase.functionsExercised) == 0
  assert testCase.fileIdsExercised is not None and file.fileID in testCase.fileIdsExercised
  assert testCase.testCaseID is not None
  assert testCase.name is not None