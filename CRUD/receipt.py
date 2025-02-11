from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class ReceiptCreate(BaseModel):
    UserID: int
    SupplierID: int | None
    TotalAmount: float
    ReceiptType: str  # 'purchase' o 'sale'
    InventoryReceiptID: int | None

class ReceiptData(ReceiptCreate):
    ReceiptID: int
    Date: str

class ReceiptCRUD:
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

    def create(self, data: ReceiptCreate):
        query = """
            INSERT INTO Receipt (UserID, SupplierID, TotalAmount, ReceiptType, InventoryReceiptID)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ReceiptID;
        """
        try:
            values = (data.UserID, data.SupplierID, data.TotalAmount, data.ReceiptType, data.InventoryReceiptID)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            receipt_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return receipt_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in receipt creation"
            )

    def update(self, id_: int, data: ReceiptData):
        query = """
            UPDATE Receipt
            SET UserID = %s, SupplierID = %s, TotalAmount = %s, ReceiptType = %s, InventoryReceiptID = %s
            WHERE ReceiptID = %s;
        """
        values = (data.UserID, data.SupplierID, data.TotalAmount, data.ReceiptType, data.InventoryReceiptID, id_)
        self._execution(query, values)

    def delete(self, id_: int):
        query = """
            DELETE FROM Receipt
            WHERE ReceiptID = %s;
        """
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int) -> ReceiptData:
        query = """
            SELECT ReceiptID, UserID, SupplierID, Date, TotalAmount, ReceiptType, InventoryReceiptID
            FROM Receipt
            WHERE ReceiptID = %s;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query, (id_,))
        receipt = cursor.fetchone()
        cursor.close()
        if receipt:
            return ReceiptData(
                ReceiptID=receipt[0],
                UserID=receipt[1],
                SupplierID=receipt[2],
                Date=str(receipt[3]),
                TotalAmount=float(receipt[4]),
                ReceiptType=receipt[5],
                InventoryReceiptID=receipt[6]
            )
        raise HTTPException(status_code=404, detail="Receipt not found")

    def get_all(self) -> List[ReceiptData]:
        query = """
            SELECT ReceiptID, UserID, SupplierID, Date, TotalAmount, ReceiptType, InventoryReceiptID
            FROM Receipt;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        receipts = cursor.fetchall()
        cursor.close()
        return [
            ReceiptData(
                ReceiptID=row[0],
                UserID=row[1],
                SupplierID=row[2],
                Date=str(row[3]),
                TotalAmount=float(row[4]),
                ReceiptType=row[5],
                InventoryReceiptID=row[6]
            )
            for row in receipts
        ]
