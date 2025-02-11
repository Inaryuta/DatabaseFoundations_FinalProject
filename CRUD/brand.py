from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


class BrandCreate(BaseModel):
    Name: str
    Country: str | None

class BrandData(BrandCreate):
    BrandID: int

class BrandCRUD:
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
            print(f"Failing in brand operation. {e}")
            raise e

    def create(self, data: BrandCreate):
        query = """
            INSERT INTO Brand (Name, Country)
            VALUES (%s, %s)
            RETURNING BrandID;
        """
        try:
            values = (data.Name, data.Country)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            brand_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return brand_id
        except IntegrityError as e:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in brand creation"
            )

    def update(self, id_: int, data: BrandData):
        query = """
            UPDATE Brand
            SET Name = %s, Country = %s
            WHERE BrandID = %s;
        """
        try:
            values = (data.Name, data.Country, id_)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in brand update. {e}")

    def delete(self, id_: int):
        query = """
            DELETE FROM Brand
            WHERE BrandID = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
        except Exception as e:
            print(f"Failing in brand delete. {e}")

    def get_by_id(self, id_: int) -> BrandData:
        query = """
            SELECT BrandID, Name, Country
            FROM Brand
            WHERE BrandID = %s;
        """
        try:
            values = (id_, )
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            brand = cursor.fetchone()
            cursor.close()
            return brand
        except Exception as e:
            print(f"Failing to get brand by id. {e}")

    def get_all(self) -> List[BrandData]:
        query = """
            SELECT *
            FROM Brand;
        """
        brands = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            brands = cursor.fetchall()
        except Exception as e:
            print(f"Fail getting all brands. {e}")

        return brands
