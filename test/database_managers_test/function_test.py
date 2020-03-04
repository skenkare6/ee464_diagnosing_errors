import sys, os, pytest, json

from Function import Function     # pylint: disable=import-error
from SourceFile import SourceFile # pylint: disable=import-error
from Database import Database     # pylint: disable=import-error

def test_create(with_database):
  containingSourceFile = SourceFile.get_by_file_path("one.r")
  created = Function.create("testFunction", containingSourceFile.fileID)

  assert created.name == "testFunction"

def test_get_by_name_and_file_id_function_exists(with_database):
  file = SourceFile.get_by_file_path("one.r")
  function = Function.get_by_name_and_file_id("doMath", file.fileID)

  assert function is not None and function.name == "doMath"

def test_get_by_name_and_file_id_function_not_exists(with_database):
  file = SourceFile.get_by_file_path("one.r")
  function = Function.get_by_name_and_file_id("1p23u1", file.fileID)

  assert function is None

def test_get_by_name_and_file_id_file_id_not_valid(with_database):
  file = SourceFile.get_by_file_path("one.r")
  function = Function.get_by_name_and_file_id("doMath", 3092190309123)

  assert function is None

def test_get_by_name_function_exists(with_database):
  file = SourceFile.get_by_file_path("one.r")
  function = Function.get_by_name("doMath")

  assert function is not None and function.name == "doMath"

def test_get_by_name_function_not_exists(with_database):
  file = SourceFile.get_by_file_path("one.r")
  function = Function.get_by_name("aopiwjdapowd")

  assert function is None

def test_gets_first_function_with_name_if_multiple_same_name(with_database):
  file = SourceFile.get_by_file_path("two.r")
  first = Function.get_by_name("doMath")
  duplicate = Function.create("doMath", file.fileID)

  assert duplicate.functionID == first.functionID

def test_get_by_name_and_file_id_returns_first_if_multiple_same_name(with_database):
  file = SourceFile.get_by_file_path("one.r")
  first = Function.get_by_name("doMath")
  duplicate = Function.create("doMath", file.fileID)

  assert duplicate.functionID == first.functionID