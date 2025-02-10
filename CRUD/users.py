from database_connection import PostgresDatabaseConnection

from typing import List
from pydantic import BaseModel

class UserData(BaseModel):
    UserID: int
    Username: str
    Password: str
    Role: int
    Email: str

class userCRUD:
    def __init__(self):
        self.db_connection = PostgresDatabaseConnection()
        self.db_connection.connect()

    def _execution(self, query: str, values: tuple):
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            self.db_connection.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Failing in the user update. {e}")

    def create(self, data: UserData):
        query = """
            INSERT INTO user (Username, Password, Role, Email)
            VALUES (%s, %s, %s, %s);
            RETURNING UserID;
        """
        try:
            values = (data.Username, data.Password, data.Role, data.Email)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return user_id
        except Exception as e:
            print(f"Failing in the user update. {e}")


    def update(self, id_: int, data: UserData):
        query = """
            UPDATE user
            SET Username = %s, Password = %s
            WHERE UserID = %s;
        """
        try:
            values = (data.Username, data.Password, id_)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user update. {e}")

    def delete(self, id_: int):
        query = """
            DELETE FROM user
            WHERE UserID = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user delete. {e}")

    def get_by_id(self, id_: int):
        query = """
            SELECT Username, Password, Role, Email
            FROM user
            WHERE UserID = %s;
        """
        try:
            values = (id_, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"Failing to get user by id. {e}")

    def get_all(self):
        query = """
            SELECT *
            FROM user;
        """
        user = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            user = cursor.fetchall()
        except Exception as e:
            print(f"Fail getting all the users. {e}")

        return user

    def get_by_name(self, name: str):
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM user
            WHERE Username LIKE  '\% %s \%';
        """
        try:
            values = (name, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchall()
            return user
        except Exception as e:
            print(f"Fail getting users by name. {e}")


    def get_by_email(self, email: str):
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM user
            WHERE email = %s;
        """
        try:
            values = (email, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Fail getting a user by email. {e}")
