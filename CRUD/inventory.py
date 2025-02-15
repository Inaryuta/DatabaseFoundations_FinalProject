from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class InventoryCreate(BaseModel):
    InstrumentID: int
    AccessoryID: int
    Quantity: int
    InventoryReceiptID: int | None

from datetime import datetime
from pydantic import BaseModel

class InventoryData(BaseModel):
    InventoryID: int
    InstrumentID: int | None
    AccessoryID: int | None
    Quantity: int
    DateUpdated: datetime  

    class Config:
        orm_mode = True


class InventoryCRUD:
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

    def create(self, data: InventoryCreate):
        query = """
            INSERT INTO Inventory (InstrumentID, AccessoryID, Quantity)
            VALUES (%s, %s, %s)
            RETURNING InventoryID;
        """
        try:
            values = (data.InstrumentID, data.AccessoryID, data.Quantity)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            inventory_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return inventory_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in inventory creation"
            )

    def update(self, id_: int, data: InventoryData):
        query = """
            UPDATE Inventory
            SET InstrumentID = %s, AccessoryID = %s, Quantity = %s
            WHERE InventoryID = %s;
        """
        values = (data.InstrumentID, data.AccessoryID, data.Quantity, id_)
        self._execution(query, values)


    def delete(self, id_: int):
        query = """
            DELETE FROM Inventory
            WHERE InventoryID = %s;
        """
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int) -> InventoryData:
        query = """
            SELECT InventoryID, InstrumentID, AccessoryID, Quantity, DateUpdated
            FROM Inventory
            WHERE InventoryID = %s;
        """
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                raise HTTPException(status_code=404, detail="Inventory not found")
            return InventoryData(
                InventoryID=row[0],
                InstrumentID=row[1],
                AccessoryID=row[2],
                Quantity=row[3],
                DateUpdated=row[4]
            )
        except Exception as e:
            print(f"Error getting inventory by id: {e}")
            raise HTTPException(status_code=400, detail="Error getting inventory")


    def get_all(self) -> List[InventoryData]:
        query = """
            SELECT InventoryID, InstrumentID, AccessoryID, Quantity, DateUpdated
            FROM Inventory
            ORDER BY InventoryID;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [
                InventoryData(
                    InventoryID=row[0],
                    InstrumentID=row[1],
                    AccessoryID=row[2],
                    Quantity=row[3],
                    DateUpdated=row[4]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Error obteniendo inventarios: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo inventarios"
            )
