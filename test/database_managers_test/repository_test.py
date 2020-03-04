import sys, os, pytest, json

from Repository import Repository  # pylint: disable=import-error
from Database import Database      # pylint: disable=import-error

def test_create(with_database):
    repository = Repository.create("path")
    
    assert repository.path == "path"

def test_get_by_path(with_database):
    Repository.create("path/hello")
    
    assert Repository.get_by_path("path/hello").path == "path/hello"

