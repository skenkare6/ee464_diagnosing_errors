import pymysql.cursors

class Database:
    def __init__(self, db, user, password):
        self.connection = pymysql.connect(host='localhost',
                                          user=user,
                                          password=password,
                                          db=db,
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def query(self, query_string):
        return self.cursor.execute(query_string)
