import pytest, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/database_managers')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/')))
from Database import Database

@pytest.fixture
def with_database():
    repo_id = create_repository()

    file1_id = create_file(repo_id, "one.r")
    file2_id = create_file(repo_id, "two.r")

    function1_id = create_function(file1_id, "doMath")
    function2_id = create_function(file2_id, "doOtherMath")
    function3_id = create_function(file1_id, "doSomeMoreMath")

    test1_id = create_test_case(file1_id, "first_test")
    test2_id = create_test_case(file1_id, "second_test")

    create_link(function1_id, test1_id)
    create_link(function1_id, test2_id)

    yield
    teardown()

# This is horrible but the best way to get tests done before everyone's code
# is in. TODO: Stop using these when we have ORM/manager classes.
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

    query_string = "select * from RFiles where filePath = '{}'".format(name)
    result = db.query(query_string)[0]
    return result['fileID']

def create_function(file_id, name):
    db = Database("test", "root", "")
    query_string = "insert into RFunctions (fileID, functionName) values \
                    ({}, '{}');".format(file_id, name)
    db.query(query_string)

    query_string = "select * from RFunctions where functionName = '{}';".format(name)
    results = db.query(query_string)[0]
    return results['functionID']

def create_test_case(file_id, name):
    db = Database("test", "root", "")
    query_string = "insert into RTestCases (fileID, testCaseName) values \
                    ({}, '{}');".format(file_id, name)
    db.query(query_string)

    query_string = "select * from RTestCases where testCaseName = '{}';".format(name)
    results = db.query(query_string)[0]
    return results['testCaseID']

def create_link(function_id, test_case_id):
    db = Database("test", "root", "")
    query_string = "insert into RCodeToTestCases (functionID, testCaseID) values \
                    ({}, {});".format(function_id, test_case_id)
    db.query(query_string)
    return True

def teardown():
    db = Database("test", "root", "")
    db.query("SET foreign_key_checks = 0;")
    db.query("delete from RCodeToTestCases where 1=1;")
    db.query("delete from RFunctions where 1=1;")
    db.query("delete from RTestCases where 1=1;")
    db.query("delete from RFiles where 1=1;")
    db.query("delete from Repositories where 1=1;")
    db.query("SET foreign_key_checks = 1;")


