import sys, os, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Database import Database

def test_gets_the_rtests(with_database):
    db = Database("test","root","")
