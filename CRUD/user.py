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
            print(f"Failing in the operation: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error during operation: {e}"
            )

    def create(self, data: UserCreate):
        query = """
            INSERT INTO users (Username, Password, Role, Email)
            VALUES (%s, %s, %s, %s)
            RETURNING UserID, Username, Password, Role, Email;
        """
        try:
            values = (data.Username, data.Password, data.Role, data.Email)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user_data = cursor.fetchone()
            self.db_connection.connection.commit()
            cursor.close()
            return UserData(**{
                "UserID": user_data[0],
                "Username": user_data[1],
                "Password": user_data[2],
                "Role": user_data[3],
                "Email": user_data[4]
            })
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
            return {"message": "User updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating user: {e}")

    def delete(self, id_: int):
        query = """
            DELETE FROM users
            WHERE UserID = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
            return {"message": "User deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting user: {e}")

    def get_by_id(self, id_: int) -> UserData:
        query = """
            SELECT Username, Password, Role, Email
            FROM users
            WHERE UserID = %s;
        """
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()
            if user:
                return UserData(**{
                    "UserID": id_,
                    "Username": user[0],
                    "Password": user[1],
                    "Role": user[2],
                    "Email": user[3]
                })
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error fetching user: {e}")

    def get_all(self) -> List[UserData]:
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM users
            ORDER BY Username;
        """
        users = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            return [UserData(**{
                "UserID": user[0],     # ID del usuario
                "Username": user[1],   # Nombre de usuario
                "Password": user[2],   # Contraseña (antes estaba omitiéndose)
                "Role": user[3],       # Rol
                "Email": user[4]       # Correo electrónico
            }) for user in users]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error fetching users: {e}")

    def get_by_name(self, name: str):
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM users
            WHERE Username ILIKE %s;
        """
        try:
            values = (f"%{name}%",)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            users = cursor.fetchall()
            cursor.close()
            return [UserData(**{
                "UserID": user[0],
                "Username": user[1],
                "Password": user[2],
                "Role": user[3],
                "Email": user[4]
            }) for user in users]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error fetching users by name: {e}")

    def get_by_email(self, email: str):
        query = """
            SELECT UserID, Username, Password, Role, Email
            FROM users
            WHERE Email = %s;
        """
        try:
            values = (email,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            user = cursor.fetchone()
            cursor.close()
            if user:
                return UserData(**{
                    "UserID": user[0],
                    "Username": user[1],
                    "Password": user[2],
                    "Role": user[3],
                    "Email": user[4]
                })
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error fetching user by email: {e}")
