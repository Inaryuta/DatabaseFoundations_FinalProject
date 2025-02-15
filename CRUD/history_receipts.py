from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class HistoryReceiptsCreate(BaseModel):
    ReceiptID: int
    Status: str  # Valores permitidos: 'completed', 'refunded'

class HistoryReceiptsData(HistoryReceiptsCreate):
    HistoryID: int
    Date: datetime

class HistoryReceiptsCRUD:
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

    def create(self, data: HistoryReceiptsCreate):
        query = """
            INSERT INTO History_Receipts (ReceiptID, Status)
            VALUES (%s, %s)
            RETURNING HistoryID;
        """
        try:
            values = (data.ReceiptID, data.Status)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            history_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return history_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in history receipt creation"
            )

    def update(self, id_: int, data: HistoryReceiptsCreate):
        query = """
            UPDATE History_Receipts
            SET ReceiptID = %s, Status = %s
            WHERE HistoryID = %s;
        """
        values = (data.ReceiptID, data.Status, id_)
        self._execution(query, values)

    def delete(self, id_: int):
        query = """
            DELETE FROM History_Receipts
            WHERE HistoryID = %s;
        """
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int) -> HistoryReceiptsData:
        query = """
            SELECT HistoryID, ReceiptID, "Date", Status
            FROM History_Receipts
            WHERE HistoryID = %s;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query, (id_,))
        history = cursor.fetchone()
        cursor.close()
        if history:
            return HistoryReceiptsData(
                HistoryID=history[0],
                ReceiptID=history[1],
                Date=str(history[2]),
                Status=history[3]
            )
        raise HTTPException(status_code=404, detail="History receipt not found")

    def get_all(self) -> List[HistoryReceiptsData]:
        query = """
            SELECT 
                HistoryID, 
                ReceiptID, 
                "Date", 
                Status
            FROM History_Receipts
            ORDER BY "Date" DESC;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        histories = cursor.fetchall()
        cursor.close()
        return [
            HistoryReceiptsData(
                HistoryID=row[0],
                ReceiptID=row[1],
                Date=row[2],  # Se asume que es un objeto datetime
                Status=row[3]
            )
            for row in histories
        ]
