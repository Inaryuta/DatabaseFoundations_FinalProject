from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


class BrandCreate(BaseModel):
    Name: str
    Country: str


class BrandData(BrandCreate):
    BrandID: int


class BrandCRUD:
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
            print(f"Error en la operación de Brand: {e}")
            raise e

    def create(self, data: BrandCreate) -> int:
        query = """
            INSERT INTO Brand (Name, Country)
            VALUES (%s, %s)
            RETURNING BrandID;
        """
        try:
            values = (data.Name, data.Country)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            brand_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return brand_id
        except IntegrityError as e:
            self.db_connection.connection.rollback()
            # Aquí se podría validar si se viola una restricción única, por ejemplo
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Error de integridad al crear la marca"
            )
        except Exception as e:
            self.db_connection.connection.rollback()
            print(f"Error creando la marca: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error en la creación de la marca: {str(e)}"
            )

    def update(self, id_: int, data: BrandCreate):
        query = """
            UPDATE Brand
            SET Name = %s, Country = %s
            WHERE BrandID = %s;
        """
        try:
            values = (data.Name, data.Country, id_)
            self._execution(query, values)
            return {"detail": "Brand updated correctly"} 
        except Exception as e:
            print(f"Error actualizando la marca: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error actualizando la marca"
            )

    def delete(self, id_: int):
        query = "DELETE FROM Brand WHERE BrandID = %s RETURNING BrandID;"
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (id_,))
            deleted = cursor.fetchone()
            self.db_connection.connection.commit()
            cursor.close()
            if deleted is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marca no encontrada")
            return {"message": "Marca eliminada exitosamente"}
        except Exception as e:
            print(f"Error eliminando la marca: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error eliminando la marca")

    def get_by_id(self, id_: int) -> BrandData:
        query = """
            SELECT BrandID, Name, Country
            FROM Brand
            WHERE BrandID = %s;
        """
        try:
            values = (id_,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Marca no encontrada"
                )
            return BrandData(BrandID=row[0], Name=row[1], Country=row[2])
        except Exception as e:
            print(f"Error obteniendo la marca por id: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo la marca"
            )

    def get_all(self, limit: int = 50, offset: int = 0) -> List[BrandData]:
        query = """
            SELECT BrandID, Name, Country
            FROM Brand
            ORDER BY Name
            LIMIT %s OFFSET %s;
        """
        try:
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()
            cursor.close()
            return [BrandData(BrandID=row[0], Name=row[1], Country=row[2]) for row in rows]
        except Exception as e:
            print(f"Error obteniendo todas las marcas: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo las marcas"
            )

    def get_by_country(self, country: str) -> List[BrandData]:
        query = """
            SELECT BrandID, Name, Country
            FROM Brand
            WHERE Country = %s;
        """
        try:
            values = (country,)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchall()
            cursor.close()
            brands = [BrandData(BrandID=row[0], Name=row[1], Country=row[2]) for row in rows]
            return brands
        except Exception as e:
            print(f"Error obteniendo marcas por país: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo marcas por país"
            )

    def get_by_name(self, name: str) -> List[BrandData]:
        query = """
            SELECT BrandID, Name, Country
            FROM Brand
            WHERE Name ILIKE %s;
        """
        try:
            values = (f"%{name}%",)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchall()
            cursor.close()
            brands = [BrandData(BrandID=row[0], Name=row[1], Country=row[2]) for row in rows]
            return brands
        except Exception as e:
            print(f"Error obteniendo marcas por nombre: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error obteniendo marcas por nombre"
            )
