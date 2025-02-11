from .database_connection import PostgresDatabaseConnection

from typing import List
from pydantic import BaseModel

class categoryData(BaseModel):
    Name: str
    Description: str

class categoryCRUD:
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
        
    def create(self, data: categoryData):
        query = """
            INSERT INTO Category (Name, Description)
            VALUES (%s, %s)
            RETURNING CategoryID;
        """
        try:
            values = (data.Name, data.Description)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            category_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return category_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Failing in the category creation. {e}")
            raise e
        
    def update(self, data: categoryData, id_: int):
        query = """
            UPDATE Category
            SET Name = %s, Description = %s
            WHERE CategoryID = %s;
        """
        try:
            values = (data.Username, data.Password, id_)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user update. {e}")

    def delete(self, id_: int):
        query = """
            DELETE FROM Category
            WHERE CategoryID = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the user update. {e}")

    def get_all(self) -> List[categoryData]:
        query = """
            SELECT * FROM Category;
        """
        category = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            category = cursor.fetchall()
        except Exception as e:
            print(f"Fail getting all the users. {e}")

        return category
    
    def get_by_name(self, name: str):
        query = """
            SELECT CategoryID, Name, Description
            FROM Category
            WHERE CategoryID ILIKE %s;
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