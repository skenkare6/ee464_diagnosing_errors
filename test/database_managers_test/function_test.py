import sys, os, pytest, json

from Function import Function
from SourceFile import SourceFile
from Database import Database

def test_create(with_database):
  containingSourceFile = SourceFile.get_by_file_path("one.r")
  created = Function.create("testFunction", containingSourceFile.fileID)

  assert created.name == "testFunction"