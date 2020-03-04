import sys, os, pytest, json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Repository import Repository
from Database import Database

def test_create(with_database):
    repository = Repository.create(1, "path")
    
    assert repository.repositoryID == 1
    assert repository.path == "path"

def test_get_by_repositoryID(with_database):
    Repository.create(24, "/hello/world")

    assert Repository.get_by_repositoryID(24).path == "/hello/world"