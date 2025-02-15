from .database_connection import PostgresDatabaseConnection

from typing import List
from pydantic import BaseModel

from pydantic import BaseModel

class categoryData(BaseModel):
    name: str
    description: str

    class Config:
        allow_population_by_field_name = True
        fields = {
            "name": {"alias": "Name"},
            "description": {"alias": "Description"}
        }


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
            values = (data.name, data.description)
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

        
    def update(self, id_: int, data: categoryData):
        query = """
            UPDATE Category
            SET Name = %s, Description = %s
            WHERE CategoryID = %s;
        """
        try:
            values = (data.name, data.description, id_)

            self._execution(query, values)
        except Exception as e:
            print(f"Failing in the category update. {e}")
            raise e


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
            SELECT CategoryID, Name, Description
            FROM Category
            ORDER BY Name
            LIMIT 10 OFFSET 0;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            # Mapea cada fila, convirtiendo las claves a minúsculas
            categories = []
            for row in rows:
                # row es una tupla: (CategoryID, Name, Description)
                # Creamos un diccionario con las claves correctas
                data = {
                    "name": row[1],
                    "description": row[2]
                }
                categories.append(categoryData(**data))
            return categories
        except Exception as e:
            print(f"Error obteniendo todas las categorías: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo las categorías"
            )


    def get_by_name(self, name: str) -> List[categoryData]:
        query = """
            SELECT CategoryID, Name, Description
            FROM Category
            WHERE Name ILIKE %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            # Formamos el patrón en Python
            pattern = f"%{name}%"
            print("Query parameter:", pattern)  # Debug: muestra el patrón
            cursor.execute(query, (pattern,))
            rows = cursor.fetchall()
            print("Rows fetched:", rows)  # Debug: muestra las filas obtenidas
            cursor.close()
            # Mapea las filas al modelo usando los nombres en minúsculas
            return [categoryData(name=row[1], description=row[2]) for row in rows]
        except Exception as e:
            print(f"Fail getting category by name. {e}")
            return []

