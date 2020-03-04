import sys, os, pytest, json

from SourceFile import SourceFile  # pylint: disable=import-error
from Database import Database      # pylint: disable=import-error

def test_gets_the_test_names(with_database):
    sourceFile = SourceFile.get_by_file_path("one.r")
    expected = set(["first_test", "second_test"])

    assert expected == set(sourceFile.testCaseNames)

def test_get_function_names_from_test_name(with_database):
    sourceFile = SourceFile.get_by_file_path("one.r")
    expected = set(["doMath", "doSomeMoreMath"])

    assert expected == set(sourceFile.functionNames)

def test_sets_file_path(with_database):
    sourceFile = SourceFile.get_by_file_path("one.r")

    assert sourceFile.filePath == "one.r"

def test_behaviour_on_not_found_filepath(with_database):
    sourceFile = SourceFile.get_by_file_path("cheese.r")

    assert len(sourceFile.testCaseNames) == 0
    assert len(sourceFile.functionNames) == 0

def test_to_json_string_has_function_names(with_database):
    sourceFile = SourceFile.get_by_file_path("one.r")
    dict = json.loads(sourceFile.to_json_string())

    assert set(sourceFile.functionNames) == set(["doMath", "doSomeMoreMath"])

def test_to_json_string_has_test_names(with_database):
    sourceFile = SourceFile.get_by_file_path("one.r")
    dict = json.loads(sourceFile.to_json_string())

    assert set(sourceFile.testCaseNames) == set(["first_test","second_test"])

def test_to_json_string_has_file_path_as_top_level(with_database):
    sourceFile = SourceFile.get_by_file_path("one.r")
    dict = json.loads(sourceFile.to_json_string())
    top_level_keys = set(dict.keys())

    assert top_level_keys == set(["one.r"])

def test_create(with_database):
    sourceFile = SourceFile.create("three.r", 1, ".")

    assert sourceFile.filePath == "three.r" and sourceFile.fileType == 1

def test_assigns_all_fields(with_database):
  sourceFile = SourceFile.create("lemons.r", 0, ".")
  assert sourceFile.filePath == "lemons.r"
  assert sourceFile.fileType == 0
  assert sourceFile.functionNames is not None
  assert sourceFile.testCaseNames is not None
  assert sourceFile.fileID is not None
