import json

from Database import Database # pylint: disable=import-error
from Repository import Repository

class SourceFile():
    def __init__(self, filePath, fileID, fileType, testCaseNames, functionNames, repoId):
        self.filePath = filePath
        self.fileType = fileType
        self.functionNames = functionNames
        self.testCaseNames = testCaseNames
        self.repositoryID = repoId
        self.fileID = fileID

    def to_json_string(self):
        dict = { self.filePath: { "tests": self.testCaseNames,
                                 "functions": self.functionNames } }
        return json.dumps(dict, indent=1)


    @staticmethod
    def create(filePath, fileType, repositoryPath):
        db = Database.getInstance()

        repo = Repository.get_by_path(repositoryPath)
        if repo is None:
          return None

        print(repo.repositoryID, filePath, fileType)
        query = "insert into RFiles (repositoryID, filePath, fileType) \
                values ({}, '{}', {});".format(repo.repositoryID, filePath, fileType)
        db.query(query)

        return SourceFile.get_by_file_path(filePath)

    @staticmethod
    def get_by_file_path(filepath):
        db = Database.getInstance()

        raw_query = "select * from RFiles \
                        left outer join RFunctions \
                            on RFunctions.fileID = RFiles.fileID \
                        left outer join RCodeToTestCases \
                            on RCodeToTestCases.functionID = RFunctions.functionID \
                        left outer join RTestCases \
                            on RTestCases.testCaseID = RCodeToTestCases.testCaseId \
                        where filePath = '{}';".format(filepath)

        results = db.query(raw_query)

        if results is None or len(results) == 0:
          return None

        testCaseNames = [record['testCaseName'] for record in results if record['testCaseName']]
        functionNames = [record['functionName'] for record in results if record['functionName']]
        repositoryID = results[0].get('repositoryID', None) if len(results) > 0 else None
        filetype = results[0].get('fileType', None) if len(results) > 0 else None
        fileID = results[0].get('fileID', None) if len(results) > 0 else None

        file = SourceFile(filepath, fileID, filetype, testCaseNames, functionNames, repositoryID)
        return file

