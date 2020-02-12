import pytest, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Database import Database

@pytest.fixture
def with_database():
    db = Database("test", "root", "")
    db.query("insert into Repositories (path) values ('.');")

    yield

    db.query("delete from Repositories where 1=1;")

