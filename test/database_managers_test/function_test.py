import sys, os, pytest, json

from Function import Function     # pylint: disable=import-error
from SourceFile import SourceFile # pylint: disable=import-error
from Database import Database     # pylint: disable=import-error

def test_create(with_database):
  containingSourceFile = SourceFile.get_by_file_path("one.r")
  created = Function.create(containingSourceFile.fileID, "testFunction")

  assert created.name == "testFunction"