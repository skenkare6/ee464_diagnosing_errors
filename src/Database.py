import pymysql.cursors

class Database:
    def __init__(self, db, user, password):
        self.connection = pymysql.connect(host='localhost',
                                          user=user,
                                          password=password,
                                          db=db,
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    # TODO: Make this not SQL injectable
    def query(self, query_string):
        with self.connection.cursor() as cursor:
            cursor.execute(query_string)

            if self.needs_commit(query_string):
                self.connection.commit()
                return None
            else:
                return cursor.fetchall()

    def needs_commit(self, query_string):
        downcased_query_string = query_string.lower()
        commands_requiring_commit = ["update", "delete", "insert"]

        for command in commands_requiring_commit:
            if command in downcased_query_string:
                return True

        return False

