import json

from Database import Database

class SourceFile():
    def __init__(self, filepath):
        self.filepath = filepath

        self.functions = [] # TODO: fill out with array of Function objects
        self.functionNames = [] # [String]

        self.testCases = [] # TODO fill out with array of TestFile objects
        self.testCaseNames = [] # [String]

    def to_json_string(self):
        dict = { self.filepath: { "tests": self.testCaseNames,
                                 "functions": self.functionNames } }
        return json.dumps(dict, indent=1)

    @staticmethod
    def create(filepath, filetype):
        pass # TODO


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

        return file

