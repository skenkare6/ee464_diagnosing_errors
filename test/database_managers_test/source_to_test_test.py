import sys, os, pytest, json

from SourceFile import SourceFile  # pylint: disable=import-error
from Database import Database      # pylint: disable=import-error

import SourceToTest                # pylint: disable=import-error

def test_gets_json(with_database):
  json_report = json.loads(SourceToTest.getJson("one.r"))
  assert set(json_report.keys()) == set(['one.r'])

  second_level_keys = set(json_report.get('one.r').keys())
  assert second_level_keys == set(['tests', 'functions'])

  functions = set(json_report.get('one.r').get('functions'))
  assert functions == set(['doMath', 'doMath', 'doSomeMoreMath'])

  tests = set(json_report.get('one.r').get('tests'))
  assert tests == set(['first_test', 'second_test'])

