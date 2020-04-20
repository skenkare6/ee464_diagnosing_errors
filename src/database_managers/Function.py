from Database import Database # pylint: disable=import-error

class Function():
    def __init__(self, name, functionID, testCaseNames):
        self.name = name
        self.functionID = functionID
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
        functionID = results[0].get('functionID', None) if len(results) > 0 else None

        return Function(funcName, functionID, testCaseNames)
      else:
        return None

    @staticmethod
    def get_by_name_and_file_id(funcName, fileID):
      db = Database.getInstance()
      query = "select * from RFunctions \
        left outer join RCodeToTestCases \
          on RFunctions.functionID = RCodeToTestCases.functionID \
        left outer join RTestCases \
          on RCodeToTestCases.testCaseID = RTestCases.testCaseID \
        where RFunctions.functionName = '{}' \
        and RFunctions.fileID = {};".format(funcName, fileID)

      results = db.query(query)

      # For now, assume only one function with funcName
      if len(results) > 0:
        testCaseNames = [record['testCaseName'] for record in results if record['testCaseName']]
        functionID = results[0].get('functionID', None) if len(results) > 0 else None

        return Function(funcName, functionID, testCaseNames)
      else:
        return None

    @staticmethod
    def create(functionName, fileID):
      db = Database.getInstance()
      query = "insert into RFunctions \
                (fileID, functionName) values \
                ({}, '{}');".format(fileID, functionName)

      result = db.query(query)
      return Function.get_by_name(functionName)

    @staticmethod
    def get_all():
      db = Database.getInstance()
      query = "select * from RFunctions;"
      results = db.query(query)

      return results