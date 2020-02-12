import pytest, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Database import Database

@pytest.fixture
def with_database():
    repo_id = create_repository()
    create_file(repo_id, "one.r")
    create_file(repo_id, "two.r")
    yield
    teardown()

def create_repository():
    db = Database("test", "root", "")
    db.query("insert into Repositories (path) values ('.');")
    repo = db.query("select * from Repositories limit 1")[0]
    return repo['repositoryID']

def create_file(repo_id, name):
    db = Database("test", "root", "")
    query_string = "insert into RFiles (repositoryID, \
            filePath, fileType) values ({}, '{}', {});".format(repo_id, name, 1)

    db.query(query_string)


def teardown():
    db = Database("test", "root", "")
    db.query("delete from RFiles where 1=1;")
    db.query("delete from Repositories where 1=1;")

