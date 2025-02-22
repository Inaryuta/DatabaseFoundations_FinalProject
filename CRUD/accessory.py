from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class AccessoryCreate(BaseModel):
    Name: str
    Description: str | None
    Price: float
    Stock: int
    CategoryID: int
    BrandID: int

class AccessoryData(AccessoryCreate):
    AccessoryID: int

class AccessoryCRUD:
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

    def create(self, data: AccessoryCreate):
        query = """
            INSERT INTO Accessory (Name, Description, Price, Stock, CategoryID, BrandID)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING AccessoryID;
        """
        try:
            values = (data.Name, data.Description, data.Price, data.Stock, data.CategoryID, data.BrandID)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            accessory_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return accessory_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in accessory creation"
            )

    def update(self, id_: int, data: AccessoryCreate):
        query = """
            UPDATE Accessory
            SET Name = %s, Description = %s, Price = %s, Stock = %s, CategoryID = %s, BrandID = %s
            WHERE AccessoryID = %s;
        """
        try:
            values = (data.Name, data.Description, data.Price, data.Stock, data.CategoryID, data.BrandID, id_)
            self._execution(query, values)
            return {"detail": "Accessory updated correctly"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating accessory: {str(e)}")

    def delete(self, id_: int):
        query = """
            DELETE FROM Accessory
            WHERE AccessoryID = %s;
        """
        try:
            self._execution(query, (id_,))
            return {"detail": "Accessory deleted successfully"}  # ✅ Mensaje de éxito
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error deleting accessory: {str(e)}")


    def get_by_id(self, id_: int) -> AccessoryData:
        query = """
            SELECT AccessoryID, Name, Description, Price, Stock, CategoryID, BrandID
            FROM Accessory
            WHERE AccessoryID = %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (id_,))
            accessory = cursor.fetchone()
            cursor.close()
            
            if accessory:
                return AccessoryData(
                    AccessoryID=accessory[0],
                    Name=accessory[1],
                    Description=accessory[2],
                    Price=accessory[3],
                    Stock=accessory[4],
                    CategoryID=accessory[5],
                    BrandID=accessory[6]
                )
            else:
                raise HTTPException(status_code=404, detail="Accessory not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving accessory: {str(e)}")

    def get_all(self) -> List[AccessoryData]:
        query = """
            SELECT AccessoryID, Name, Description, Price, Stock, CategoryID, BrandID
            FROM Accessory
            ORDER BY Name;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query)
            accessories = cursor.fetchall()
            cursor.close()

            return [
                AccessoryData(
                    AccessoryID=row[0],
                    Name=row[1],
                    Description=row[2],
                    Price=row[3],
                    Stock=row[4],
                    CategoryID=row[5],
                    BrandID=row[6]
                )
                for row in accessories
            ]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error retrieving accessories: {str(e)}")
