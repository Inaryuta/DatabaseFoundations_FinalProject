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

class ReceiptData(BaseModel):
    ReceiptID: int
    UserID: int
    SupplierID: int | None
    Date: str  # cadena en formato ISO
    TotalAmount: float
    ReceiptType: str


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

    def create(self, data: ReceiptData) -> int:
        query = """
            INSERT INTO Receipt (UserID, SupplierID, TotalAmount, ReceiptType)
            VALUES (%s, %s, %s, %s)
            RETURNING ReceiptID;
        """
        try:
            values = (data.UserID, data.SupplierID, data.TotalAmount, data.ReceiptType)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            receipt_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return receipt_id
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creando receipt: {e}")
            raise e


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
            SELECT ReceiptID, UserID, SupplierID, "Date", TotalAmount, ReceiptType
            FROM Receipt
            WHERE ReceiptID = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (id_,))
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                raise HTTPException(status_code=404, detail="Receipt not found")
            return ReceiptData(
                ReceiptID=row[0],
                UserID=row[1],
                SupplierID=row[2],
                Date=row[3],
                TotalAmount=row[4],
                ReceiptType=row[5]
            )
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error getting receipt by id: {e}")
            raise HTTPException(status_code=400, detail="Error getting receipt")


    def get_all(self) -> List[ReceiptData]:
        query = """
            SELECT 
                ReceiptID,
                UserID,
                SupplierID,
                to_char("Date", 'YYYY-MM-DD"T"HH24:MI:SS') as Date_str,
                TotalAmount,
                ReceiptType
            FROM Receipt
            ORDER BY "Date" DESC;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return [
                ReceiptData(
                    ReceiptID=row[0],
                    UserID=row[1],
                    SupplierID=row[2],
                    Date=row[3],
                    TotalAmount=row[4],
                    ReceiptType=row[5]
                )
                for row in rows
            ]
        except Exception as e:
            print(f"Error obteniendo recibos: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo recibos"
            )
