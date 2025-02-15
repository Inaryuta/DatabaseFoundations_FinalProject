from .database_connection import PostgresDatabaseConnection
from typing import List, Optional
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from psycopg2 import IntegrityError, DatabaseError
from datetime import datetime

class ReceiptCreate(BaseModel):
    UserID: Optional[int] = None
    SupplierID: Optional[int] = None
    TotalAmount: float
    ReceiptType: str  # 'purchase' o 'sale'
    InventoryReceiptID: Optional[int] = None

class ReceiptData(BaseModel):
    ReceiptID: int
    UserName: Optional[str] = None
    SupplierName: Optional[str] = None
    ItemName: Optional[str] = None
    Date: datetime
    TotalAmount: float
    ReceiptType: str
    UserID: Optional[int] = None
    SupplierID: Optional[int] = None
    InventoryReceiptID: Optional[int] = None

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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while executing the database operation."
            )

    def create(self, data: ReceiptCreate):
        # Validar que solo una de las llaves (UserID o SupplierID) esté presente
        if (data.UserID is not None and data.SupplierID is not None) or (data.UserID is None and data.SupplierID is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either UserID or SupplierID must be provided, but not both."
            )

        query_insert = """
            INSERT INTO Receipt (UserID, SupplierID, TotalAmount, ReceiptType, InventoryReceiptID)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ReceiptID;
        """

        try:
            with self.db_connection.connection.cursor() as cursor:

                # Verificar si InventoryReceiptID fue proporcionado y existe en la BD
                if data.InventoryReceiptID is not None:
                    query_check_inventory = "SELECT 1 FROM Inventory_Receipt WHERE InventoryReceiptID = %s;"
                    cursor.execute(query_check_inventory, (data.InventoryReceiptID,))
                    if cursor.fetchone() is None:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"InventoryReceiptID {data.InventoryReceiptID} does not exist."
                        )

                # Insertar el nuevo recibo
                values = (data.UserID, data.SupplierID, data.TotalAmount, data.ReceiptType, data.InventoryReceiptID)
                cursor.execute(query_insert, values)
                receipt_id = cursor.fetchone()[0]

            self.db_connection.connection.commit()
            return receipt_id

        except IntegrityError as e:
            self.db_connection.connection.rollback()
            print(f"IntegrityError: {e}")  # <-- Esto imprimirá el error real en la consola
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)  # <-- Muestra el mensaje real en Postman
            )

        except DatabaseError as db_error:
            self.db_connection.connection.rollback()
            if "relation \"inventoryreceipt\" does not exist" in str(db_error).lower():
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Table 'Inventory_Receipt' does not exist in the database."
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred."
            )

        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creating receipt: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the receipt."
            )

    def update(self, receipt_id: int, data: dict):
        try:
            cursor = self.db_connection.connection.cursor()

            # Verificar si el Receipt existe
            query_check = "SELECT 1 FROM Receipt WHERE ReceiptID = %s;"
            cursor.execute(query_check, (receipt_id,))
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Receipt with ID {receipt_id} not found."
                )

            # Construir dinámicamente la consulta de actualización
            update_fields = []
            values = []
            if data.UserID is not None:
                update_fields.append("UserID = %s")
                values.append(data.UserID)
            if data.SupplierID is not None:
                update_fields.append("SupplierID = %s")
                values.append(data.SupplierID)
            if data.TotalAmount is not None:
                update_fields.append("TotalAmount = %s")
                values.append(data.TotalAmount)
            if data.ReceiptType is not None:
                update_fields.append("ReceiptType = %s")
                values.append(data.ReceiptType)

            # Si no se envió ningún campo válido, lanzar un error
            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No valid fields provided for update."
                )

            # Construir y ejecutar la consulta SQL
            query_update = f"""
                UPDATE Receipt
                SET {', '.join(update_fields)}
                WHERE ReceiptID = %s;
            """
            values.append(receipt_id)
            cursor.execute(query_update, tuple(values))
            self.db_connection.connection.commit()
            cursor.close()
        
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Integrity constraint violated while updating receipt."
            )

        except DatabaseError as db_error:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(db_error)}"
            )

        except Exception as e:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
    
    def delete(self, id_: int):
        query_check = "SELECT 1 FROM Receipt WHERE ReceiptID = %s;"
        query_delete = "DELETE FROM Receipt WHERE ReceiptID = %s;"

        cursor = self.db_connection.connection.cursor()
        cursor.execute(query_check, (id_,))
        exists = cursor.fetchone()

        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with ID = {id_} not found"
            )

        self._execution(query_delete, (id_,))
        return {"message": f"Receipt with ID = {id_} deleted successfully"}

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
                SupplierID=receipt[2] if receipt[2] is not None else None,
                Date=str(receipt[3]),
                TotalAmount=float(receipt[4]),
                ReceiptType=receipt[5],
                InventoryReceiptID=receipt[6] if receipt[6] is not None else None
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )

    def get_all(self) -> List[ReceiptData]:
        query = """
            SELECT R.ReceiptID, R.UserID, COALESCE(R.SupplierID, NULL) AS SupplierID, R.Date,
                   R.TotalAmount, R.ReceiptType, COALESCE(R.InventoryReceiptID, NULL) AS InventoryReceiptID
            FROM Receipt R
            ORDER BY R.Date DESC
            LIMIT 10 OFFSET 0;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        receipts = cursor.fetchall()
        cursor.close()

        if not receipts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No receipts found"
            )

        return [
            ReceiptData(
                ReceiptID=row[0],
                UserID=row[1],
                SupplierID=row[2] if row[2] is not None else None,
                Date=str(row[3]),
                TotalAmount=float(row[4]),
                ReceiptType=row[5],
                InventoryReceiptID=row[6] if row[6] is not None else None
            )
            for row in receipts
        ]

    def get_receipt_details(self):
            query = """
            SELECT 
                R.ReceiptID, 
                U.Username AS UserName, 
                COALESCE(S.Name, 'No Supplier') AS SupplierName, 
                COALESCE(I.Name, A.Name, 'No Item') AS ItemName,
                R.Date, 
                R.TotalAmount, 
                R.ReceiptType
            FROM Receipt R
            LEFT JOIN users U ON R.UserID = U.UserID
            LEFT JOIN Supplier S ON R.SupplierID = S.SupplierID
            LEFT JOIN Inventory_Receipt IR ON R.InventoryReceiptID = IR.InventoryReceiptID
            LEFT JOIN Inventory Inv ON IR.InventoryID = Inv.InventoryID
            LEFT JOIN Instrument I ON Inv.InstrumentID = I.InstrumentID
            LEFT JOIN Accessory A ON Inv.AccessoryID = A.AccessoryID
            ORDER BY R.Date DESC;
            """
            
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            receipts = cursor.fetchall()
            cursor.close()

            return [
                {
                    "ReceiptID": row[0],
                    "UserName": row[1],
                    "SupplierName": row[2],
                    "ItemName": row[3],
                    "Date": str(row[4]),
                    "TotalAmount": float(row[5]),
                    "ReceiptType": row[6]
                }
                for row in receipts
            ]