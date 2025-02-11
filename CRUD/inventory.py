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

class InventoryData(InventoryCreate):
    InventoryID: int
    DateUpdated: str

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
            INSERT INTO Inventory (InstrumentID, AccessoryID, Quantity, InventoryReceiptID)
            VALUES (%s, %s, %s, %s)
            RETURNING InventoryID;
        """
        try:
            values = (data.InstrumentID, data.AccessoryID, data.Quantity, data.InventoryReceiptID)
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
            SET InstrumentID = %s, AccessoryID = %s, Quantity = %s, InventoryReceiptID = %s
            WHERE InventoryID = %s;
        """
        values = (data.InstrumentID, data.AccessoryID, data.Quantity, data.InventoryReceiptID, id_)
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
            SELECT InventoryID, InstrumentID, AccessoryID, Quantity, DateUpdated, InventoryReceiptID
            FROM Inventory
            WHERE InventoryID = %s;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query, (id_,))
        inventory = cursor.fetchone()
        cursor.close()
        if inventory:
            return InventoryData(
                InventoryID=inventory[0],
                InstrumentID=inventory[1],
                AccessoryID=inventory[2],
                Quantity=inventory[3],
                DateUpdated=str(inventory[4]),
                InventoryReceiptID=inventory[5]
            )
        raise HTTPException(status_code=404, detail="Inventory item not found")

    def get_all(self) -> List[InventoryData]:
        query = """
            SELECT InventoryID, InstrumentID, AccessoryID, Quantity, DateUpdated, InventoryReceiptID
            FROM Inventory;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        inventories = cursor.fetchall()
        cursor.close()
        return [
            InventoryData(
                InventoryID=row[0],
                InstrumentID=row[1],
                AccessoryID=row[2],
                Quantity=row[3],
                DateUpdated=str(row[4]),
                InventoryReceiptID=row[5]
            )
            for row in inventories
        ]
