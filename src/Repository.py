# This is an interface to query/insert from/into the 'Repositories' table.
# get_by_repositoryID takes in a repository's ID and returns a Repository 
# class, if it exists, else it returns None.
# create takes in a repository's ID and returns a Repository class.

from Database import Database

class Repository():
    def __init__(self, repositoryID, path):
        self.repositoryID = repositoryID
        self.path = path

    @staticmethod
    def get_by_repositoryID(repositoryID):
        db = Database.getInstance()
        query = "select * from Repositories where repositoryID = \
                 {}".format(repositoryID)

        results = db.query(query)

        if len(results) > 0:
            repository = Repository(results[0]['repositoryID'], results[0]['path'])
            return repository
        else:
            return None

    @staticmethod
    def create(repositoryID, path):
        db = Database.getInstance()
        query = "insert into Repositories \
                 (repositoryID, path) values \
                 ({}, '{}');".format(repositoryID, path)

        # TODO: check if query was successful?
        result = db.query(query)
        return Repository.get_by_repositoryID(repositoryID)
