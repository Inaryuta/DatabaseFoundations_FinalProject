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
        # Verificar existencia de InventoryID y ReceiptID
        query_check_inventory = "SELECT 1 FROM Inventory WHERE InventoryID = %s;"
        query_check_receipt = "SELECT 1 FROM Receipt WHERE ReceiptID = %s;"
        
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query_check_inventory, (data.InventoryID,))
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"InventoryID {data.InventoryID} does not exist"
                )

            cursor.execute(query_check_receipt, (data.ReceiptID,))
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"ReceiptID {data.ReceiptID} does not exist"
                )

            query = """
                INSERT INTO Inventory_Receipt (InventoryID, ReceiptID, Quantity)
                VALUES (%s, %s, %s)
                RETURNING InventoryReceiptID;
            """
            values = (data.InventoryID, data.ReceiptID, data.Quantity)
            cursor.execute(query, values)
            inventory_receipt_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return inventory_receipt_id
        except IntegrityError as e:
            self.db_connection.connection.rollback()
            print(f"IntegrityError: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in inventory receipt creation"
            )
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating inventory receipt: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the inventory receipt: {e}"
            )

    def update(self, id_: int, data: InventoryReceiptData):
        # Verificar existencia de InventoryReceiptID
        query_check = "SELECT 1 FROM Inventory_Receipt WHERE InventoryReceiptID = %s;"
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query_check, (id_,))
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"InventoryReceiptID {id_} does not exist"
                )

            query = """
                UPDATE Inventory_Receipt
                SET InventoryID = %s, ReceiptID = %s, Quantity = %s
                WHERE InventoryReceiptID = %s;
            """
            values = (data.InventoryID, data.ReceiptID, data.Quantity, id_)
            self._execution(query, values)

            return {"message": f"InventoryReceiptID {id_} updated successfully"}

        except Exception as e:
            print(f"Error updating inventory receipt: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating inventory receipt: {e}"
            )
        
    def delete(self, id_: int):
        # Verificar si el InventoryReceiptID existe
        query_check = "SELECT 1 FROM Inventory_Receipt WHERE InventoryReceiptID = %s;"
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query_check, (id_,))
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"InventoryReceiptID {id_} does not exist"
                )
            query = """
                DELETE FROM Inventory_Receipt
                WHERE InventoryReceiptID = %s;
            """
            values = (id_,)
            self._execution(query, values)
            return {"message": f"InventoryReceiptID {id_} deleted successfully."}
        except Exception as e:
            print(f"Error deleting inventory receipt: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting inventory receipt: {e}"
            )

    def get_by_id(self, id_: int) -> dict:
        query = """
            SELECT InventoryReceiptID, InventoryID, ReceiptID, Quantity
            FROM Inventory_Receipt
            WHERE InventoryReceiptID = %s;
        """
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            inventory_receipt = cursor.fetchone()
            cursor.close()

            if inventory_receipt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"InventoryReceiptID {id_} not found"
                )

            return {
                "InventoryReceiptID": inventory_receipt[0],
                "InventoryID": inventory_receipt[1],
                "ReceiptID": inventory_receipt[2],
                "Quantity": inventory_receipt[3]
            }

        except Exception as e:
            print(f"Error getting inventory receipt by id: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting inventory receipt by id: {e}"
            )

    def get_all(self) -> List[dict]:
        query = """
            SELECT InventoryReceiptID, InventoryID, ReceiptID, Quantity
            FROM Inventory_Receipt
            ORDER BY InventoryReceiptID ASC;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            inventory_receipts = cursor.fetchall()
            cursor.close()

            if not inventory_receipts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No inventory receipts found"
                )

            return [
                {
                    "InventoryReceiptID": receipt[0],
                    "InventoryID": receipt[1],
                    "ReceiptID": receipt[2],
                    "Quantity": receipt[3]
                }
                for receipt in inventory_receipts
            ]

        except Exception as e:
            print(f"Error getting all inventory receipts: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting all inventory receipts: {e}"
            )

