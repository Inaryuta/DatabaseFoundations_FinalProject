from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class InventoryReceiptCreate(BaseModel):
    InventoryID: int
    ReceiptID: int
    Quantity: int

class InventoryReceiptData(InventoryReceiptCreate):
    InventoryReceiptID: int

class inventoryReceiptCRUD:
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
            print(f"Error in inventory receipt operation: {e}")
            raise e

    def create(self, data: InventoryReceiptData) -> int:
        query = """
            INSERT INTO Inventory_Receipt (InventoryID, ReceiptID, Quantity)
            VALUES (%s, %s, %s)
            RETURNING InventoryReceiptID;
        """
        try:
            values = (data.InventoryID, data.ReceiptID, data.Quantity)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            inventory_receipt_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return inventory_receipt_id
        except Exception as e:
            self.db_connection.connection.rollback()  # Aquí se limpia la transacción
            print(f"Error creating inventory receipt: {e}")
            raise e



    def update(self, id_: int, data: InventoryReceiptData):
        query = """
            UPDATE Inventory_Receipt
            SET InventoryID = %s, ReceiptID = %s, Quantity = %s
            WHERE InventoryReceiptID = %s;
        """
        try:
            values = (data.InventoryID, data.ReceiptID, data.Quantity, id_)
            self._execution(query, values)
        except Exception as e:
            print(f"Error updating inventory receipt: {e}")

    def delete(self, id_: int):
        query = """
            DELETE FROM Inventory_Receipt
            WHERE InventoryReceiptID = %s;
        """
        try:
            values = (id_,)
            self._execution(query, values)
        except Exception as e:
            print(f"Error deleting inventory receipt: {e}")

    def get_by_id(self, id_: int) -> InventoryReceiptData:
        query = """
            SELECT InventoryReceiptID, InventoryID, ReceiptID, Quantity
            FROM Inventory_Receipt
            WHERE InventoryReceiptID = %s;
        """
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                raise HTTPException(status_code=404, detail="Inventory receipt not found")
            return InventoryReceiptData(
                InventoryReceiptID=row[0],
                InventoryID=row[1],
                ReceiptID=row[2],
                Quantity=row[3]
            )
        except Exception as e:
            print(f"Error getting inventory receipt by id: {e}")
            raise HTTPException(status_code=400, detail="Error getting inventory receipt")


    def get_all(self) -> List[InventoryReceiptData]:
        query = """
            SELECT InventoryReceiptID, InventoryID, ReceiptID, Quantity
            FROM Inventory_Receipt
            ORDER BY InventoryReceiptID DESC
            LIMIT 10 OFFSET 0;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [
                InventoryReceiptData(
                    InventoryReceiptID=row[0],
                    InventoryID=row[1],
                    ReceiptID=row[2],
                    Quantity=row[3]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Error getting all inventory receipts: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error getting inventory receipts"
            )
