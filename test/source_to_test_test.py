import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Database import Database

def test_gets_the_rtests(with_database):
    pass

def test_get_function_names_from_test_name(with_database):
    db = Database("test","root","")

    raw_query = "select * \
                from RFiles \
                left outer join RFunctions \
                    on RFunctions.fileID = RFiles.fileID \
                where filePath = '{}';".format("one.r")

    results = db.query(raw_query)
    function_names = [record['functionName'] for record in results]
    expected = set(["doMath", "doSomeMoreMath"])
    assert expected == set(function_names)
