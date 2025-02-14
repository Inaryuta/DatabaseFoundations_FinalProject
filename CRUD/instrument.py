from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class InstrumentCreate(BaseModel):
    Name: str
    Description: str | None
    Price: float
    Stock: int
    CategoryID: int
    BrandID: int

class InstrumentData(InstrumentCreate):
    InstrumentID: int

class InstrumentCRUD:
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
            print(f"Database operation failed. {e}")
            raise e

    def create(self, data: InstrumentCreate):
        query = """
            INSERT INTO Instrument (Name, Description, Price, Stock, CategoryID, BrandID)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING InstrumentID;
        """
        try:
            values = (data.Name, data.Description, data.Price, data.Stock, data.CategoryID, data.BrandID)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            instrument_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return instrument_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in instrument creation"
            )

    def update(self, id_: int, data: InstrumentData):
        query = """
            UPDATE Instrument
            SET Name = %s, Description = %s, Price = %s, Stock = %s, CategoryID = %s, BrandID = %s
            WHERE InstrumentID = %s;
        """
        values = (data.Name, data.Description, data.Price, data.Stock, data.CategoryID, data.BrandID, id_)
        self._execution(query, values)

    def delete(self, id_: int):
        query = """
            DELETE FROM Instrument
            WHERE InstrumentID = %s;
        """
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int) -> InstrumentData:
        query = """
            SELECT InstrumentID, Name, Description, Price, Stock, CategoryID, BrandID
            FROM Instrument
            WHERE InstrumentID = %s;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query, (id_,))
        instrument = cursor.fetchone()
        cursor.close()
        if instrument:
            return InstrumentData(
                InstrumentID=instrument[0],
                Name=instrument[1],
                Description=instrument[2],
                Price=instrument[3],
                Stock=instrument[4],
                CategoryID=instrument[5],
                BrandID=instrument[6]
            )
        raise HTTPException(status_code=404, detail="Instrument not found")

    def get_all(self) -> List[InstrumentData]:
        query = """
            SELECT I.InstrumentID, I.Name, I.Description, I.Price, I.Stock,
               C.Name AS Category, B.Name AS Brand
        FROM Instrument I
        JOIN Category C ON I.CategoryID = C.CategoryID 
        JOIN Brand B ON I.BrandID = B.BrandID          
        ORDER BY I.Name
        LIMIT 10 OFFSET 0; 
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        instruments = cursor.fetchall()
        cursor.close()
        return [
            InstrumentData(
                InstrumentID=row[0],
                Name=row[1],
                Description=row[2],
                Price=row[3],
                Stock=row[4],
                CategoryID=row[5],
                BrandID=row[6]
            )
            for row in instruments
        ]
