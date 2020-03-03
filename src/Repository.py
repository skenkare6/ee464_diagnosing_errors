# This is an interface to query/insert from/into the 'Repositories' table.
# get_by_repositoryID takes in a repository's ID and returns a Repository 
# class.

from Database import Database

class Repository:
    def __init__(self, repositoryID, path):
        self.repositoryID = repositoryID
        self.path = path

    def get_by_repositoryID(repositoryID):
        db = Database("test", "root", "")
        repositoryTable = db.query("select * from Repositories where repositoryID = {}".format(repositoryID))
        repository = Repository(repositoryTable[0]['repositoryID'], repositoryTable[0]['path'])
        return repository
