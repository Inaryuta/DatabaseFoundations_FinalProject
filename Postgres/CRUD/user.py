from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


class UserCreate(BaseModel):
    Username: str
    Password: str
    Role: str  # "administrator" o "customer"
    Email: str

class UserData(UserCreate):
    UserID: int

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
            self.db_connection.connection.rollback()
            print(f"Failing in the user update. {e}")
            raise e

    def create(self, data: UserCreate):
        
        query = """
            INSERT INTO users (Username, Password, Role, Email)
            VALUES (%s, %s, %s, %s)
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
        except IntegrityError as e:
            self.db_connection.connection.rollback()
            if "users_username_key" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El username ya existe"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error en la creación del usuario"
                )


    def update(self, id_: int, data: UserData):
        query = """
            UPDATE users
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
            DELETE FROM users
            WHERE UserID = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user delete. {e}")

    def get_by_id(self, id_: int) -> UserData:
        query = """
            SELECT Username, Password, Role, Email
            FROM users
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

    def get_all(self) -> List[UserData]:
   
        query = """
            SELECT *
            FROM users;
        """
        users = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            users = cursor.fetchall()
        except Exception as e:
            print(f"Fail getting all the users. {e}")

        return users

    def get_by_name(self, name: str):
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM users
            WHERE Username ILIKE %s;
        """
        try:
            values = (f"%{name}%", )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            users = cursor.fetchall()
            cursor.close()
            return users
        except Exception as e:
            print(f"Fail getting users by name. {e}")



    def get_by_email(self, email: str):
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM users
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