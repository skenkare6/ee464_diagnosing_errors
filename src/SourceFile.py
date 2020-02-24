import json

from Database import Database

class SourceFile():
    def __init__(self, filepath):
        self.filepath = filepath
        self.fileType = None

        self.functions = [] # TODO: fill out with array of Function objects
        self.functionNames = [] # [String]

        self.testCases = [] # TODO fill out with array of TestFile objects
        self.testCaseNames = [] # [String]

        self.repositoryID = None

    def to_json_string(self):
        dict = { self.filepath: { "tests": self.testCaseNames,
                                 "functions": self.functionNames } }
        return json.dumps(dict, indent=1)


    @staticmethod
    def create(filePath, fileType, repositoryPath):
        db = Database.getInstance()
        results = db.query("select * from Repositories where path = '{}';".format(repositoryPath))

        if results and len(results) > 0:
            repoId = results[0]['repositoryID']

            query = "insert into RFiles (repositoryID, filePath, fileType) \
                    values ({}, '{}', '{}');".format(repoId, filePath, fileType)
            db.query(query)

            return SourceFile.get_by_file_path(filePath)
        else:
            pass


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

        file = SourceFile(filepath)
        file.testCaseNames = [record['testCaseName'] for record in results if record['testCaseName']]
        file.functionNames = [record['functionName'] for record in results if record['functionName']]
        file.repositoryID = results[0].get('repositoryID', None) if len(results) > 0 else None
        file.filetype = results[0].get('fileType', None) if len(results) > 0 else None

        return file

