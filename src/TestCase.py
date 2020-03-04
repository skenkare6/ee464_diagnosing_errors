from Database import Database
import json

class TestCase():
  def __init__(self, name, functionsExercised, filesExercised):
    self.filesExercised = filesExercised
    self.functionsExercised = functionsExercised
    self.name = name

  def to_json(self):
    json_hash = { self.name: {
      "functions": self.functionsExercised,
      "files": self.filesExercised
    }}
    return json.dumps(json_hash, indent=1)

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

    if len(results) > 0:
      filesExercised = [record['filePath'] for record in results if record['filePath']]
      functionsExercised = [record['functionName'] for record in results if record['functionName']]
      return TestCase(testCaseName, functionsExercised, filesExercised)
    else:
      return None

  @staticmethod
  def create():
    pass # TODO: