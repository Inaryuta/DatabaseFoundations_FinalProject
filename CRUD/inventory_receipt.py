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

    def create(self, data: InventoryReceiptCreate):
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
        except IntegrityError as e:
            self.db_connection.connection.rollback()
            if "inventory_receipt_inventory_id_fkey" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El InventoryID no existe"
                )
            elif "inventory_receipt_receipt_id_fkey" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El ReceiptID no existe"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error en la creación del recibo de inventario"
                )

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
            SELECT InventoryID, ReceiptID, Quantity
            FROM Inventory_Receipt
            WHERE InventoryReceiptID = %s;
        """
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            inventory_receipt = cursor.fetchone()
            cursor.close()
            return inventory_receipt
        except Exception as e:
            print(f"Error getting inventory receipt by id: {e}")

    def get_all(self) -> List[InventoryReceiptData]:
        query = """
             SELECT IR.InventoryID, R.TotalAmount, IR.Quantity
        FROM Inventory_Receipt IR
        JOIN Receipt R ON IR.ReceiptID = R.ReceiptID  
        ORDER BY R.Date DESC
        LIMIT 10 OFFSET 0;
        """
        inventory_receipts = []
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            inventory_receipts = cursor.fetchall()
        except Exception as e:
            print(f"Error getting all inventory receipts: {e}")
        return inventory_receipts
