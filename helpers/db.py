import sqlite3


class DataBase:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)

    def list_test_cases(self):
        c = self.connection.cursor()
        c.execute("SELECT * FROM tcm_testcase")
        return c.fetchall()

    def delete_test_case(self, name: str):
        c = self.connection.cursor()
        c.execute("DELETE FROM tcm_testcase WHERE name=?", (name,))
        self.connection.commit()

    def close(self):
        self.connection.close()
