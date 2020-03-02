import sys, os, pytest, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Function import Function
from SourceFile import SourceFile
from Database import Database

def test_create(with_database):
  containingSourceFile = SourceFile.get_by_file_path("one.r")
  created = Function.create(containingSourceFile.fileID, "testFunction")

  assert created.name == "testFunction"