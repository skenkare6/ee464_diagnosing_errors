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

            if self.is_effectful_query(query_string):
                self.connection.commit()
                return None
            else:
                return cursor.fetchall()

    def is_effectful_query(self, query_string):
        downcased_query_string = query_string.lower()
        effectful_commands = ["update", "delete", "insert"]

        is_effectful = False

        for command in effectful_commands:
            is_effectful = is_effectful or (command in downcased_query_string)

        return is_effectful

