from Database import Database # pylint: disable=import-error
import json

class TestCase():
  def __init__(self, id, name, functionsExercised, filesExercised, fileIdsExercised):
    self.filesExercised = filesExercised
    self.functionsExercised = functionsExercised
    self.fileIdsExercised = fileIdsExercised
    self.testCaseID = id
    self.name = name

  def to_json(self):
    json_hash = { self.name: {
      "functions": self.functionsExercised,
      "files": self.filesExercised
    }}
    return json.dumps(json_hash, indent=1)

  def create_mapping(self, function):
    if not function or not function.functionID:
      return

    db = Database.getInstance()
    query = "insert into RCodeToTestCases \
              (functionID, testCaseID) \
             values \
              ({}, {});".format(function.functionID, self.testCaseID)

    db.query(query)

  def delete_mapping(self, function):
    if not function or not function.functionID:
      return

    db = Database.getInstance()
    query = "delete from RCodeToTestCases \
              where RCodeToTestCases.functionID = {} and \
              RCodeToTestCases.testCaseID = {};".format(function.functionID, self.testCaseID)

    db.query(query)

  @staticmethod
  def get_by_name(testCaseName):
    db = Database.getInstance()
    query = "select * from RTestCases \
            left outer join RCodeToTestCases \
              on RTestCases.testCaseID = RCodeToTestCases.testCaseID \
            left outer join RFunctions \
              on RCodeToTestCases.functionID = RFunctions.functionID \
            left outer join RFiles \
              on RFunctions.fileID = RFiles.fileID \
            where RTestCases.testCaseName = '{}';".format(testCaseName)

    results = db.query(query)

    if results and len(results) > 0:
      filesExercised = [record['filePath'] for record in results if record['filePath']]
      fileIdsExercised = list(set([record['fileID'] for record in results if record['fileID']]))
      functionsExercised = [record['functionName'] for record in results if record['functionName']]
      testCaseID = results[0].get('testCaseID', None) if len(results) > 0 else None

      return TestCase(testCaseID, testCaseName, functionsExercised, filesExercised, fileIdsExercised)
    else:
      return None

  @staticmethod
  def get_by_name_and_file_id(testCaseName, fileID):
    assert testCaseName is not None
    assert fileID is not None

    db = Database.getInstance()
    query = "select * from RTestCases \
            left outer join RCodeToTestCases \
              on RTestCases.testCaseID = RCodeToTestCases.testCaseID \
            left outer join RFunctions \
              on RCodeToTestCases.functionID = RFunctions.functionID \
            left outer join RFiles \
              on RFunctions.fileID = RFiles.fileID \
            where RTestCases.testCaseName = '{}' \
            and RTestCases.fileID = {};".format(testCaseName, fileID)

    results = db.query(query)

    if results and len(results) > 0:
      filesExercised = [record['filePath'] for record in results if record['filePath']]
      functionsExercised = [record['functionName'] for record in results if record['functionName']]
      fileIdsExercised = list(set([record['fileID'] for record in results if record['fileID']]))
      testCaseID = results[0].get('testCaseID', None) if len(results) > 0 else None

      return TestCase(testCaseID, testCaseName, functionsExercised, filesExercised, fileIdsExercised)
    else:
      return None

  @staticmethod
  def create(testName, fileID):
    db = Database.getInstance()

    query = "insert into RTestCases \
              (fileID, testCaseName) \
             values \
              ({}, '{}');".format(fileID, testName)

    db.query(query)

    return TestCase.get_by_name_and_file_id(testName, fileID)