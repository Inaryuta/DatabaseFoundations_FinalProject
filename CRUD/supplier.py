from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class SupplierCreate(BaseModel):
    Name: str
    Address: str | None
    ContactInfo: str

class SupplierData(SupplierCreate):
    SupplierID: int

class SupplierCRUD:
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

    def create(self, data: SupplierCreate):
        query = """
            INSERT INTO Supplier (Name, Address, ContactInfo)
            VALUES (%s, %s, %s)
            RETURNING SupplierID;
        """
        try:
            values = (data.Name, data.Address, data.ContactInfo)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            supplier_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return supplier_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in supplier creation"
            )

    def update(self, id_: int, data: SupplierData):
        query = """
            UPDATE Supplier
            SET Name = %s, Address = %s, ContactInfo = %s
            WHERE SupplierID = %s;
        """
        values = (data.Name, data.Address, data.ContactInfo, id_)
        self._execution(query, values)

    def delete(self, id_: int):
        query = """
            DELETE FROM Supplier
            WHERE SupplierID = %s;
        """
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int) -> SupplierData:
        query = """
            SELECT SupplierID, Name, Address, ContactInfo
            FROM Supplier
            WHERE SupplierID = %s;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query, (id_,))
        supplier = cursor.fetchone()
        cursor.close()
        if supplier:
            return SupplierData(
                SupplierID=supplier[0],
                Name=supplier[1],
                Address=supplier[2],
                ContactInfo=supplier[3]
            )
        raise HTTPException(status_code=404, detail="Supplier not found")

    def get_all(self) -> List[SupplierData]:
        query = """
            SELECT SupplierID, Name, Address, ContactInfo
            FROM Supplier;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        suppliers = cursor.fetchall()
        cursor.close()
        return [
            SupplierData(
                SupplierID=row[0],
                Name=row[1],
                Address=row[2],
                ContactInfo=row[3]
            )
            for row in suppliers
        ]
