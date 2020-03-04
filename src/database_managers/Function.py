from Database import Database

class Function():
    def __init__(self, name, testCaseNames):
        self.name = name
        self.testCaseNames = testCaseNames

    @staticmethod
    def get_by_name(funcName):
      db = Database.getInstance()
      query = "select * from RFunctions \
              left outer join RCodeToTestCases \
                on RFunctions.functionID = RCodeToTestCases.functionID \
              left outer join RTestCases \
                on RCodeToTestCases.testCaseID = RTestCases.testCaseID \
              where RFunctions.functionName = '{}';".format(funcName)

      results = db.query(query)

      if len(results) > 0:
        testCaseNames = [record['testCaseName'] for record in results if record['testCaseName']]
        return Function(funcName, testCaseNames)
      else:
        return None

    @staticmethod
    def create(fileID, functionName):
      db = Database.getInstance()
      query = "insert into RFunctions \
                (fileID, functionName) values \
                ({}, '{}');".format(fileID, functionName)

      result = db.query(query)
      return Function.get_by_name(functionName)