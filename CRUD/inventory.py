from .database_connection import PostgresDatabaseConnection
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import logging

# Configuración de logging para el control de errores
logging.basicConfig(level=logging.ERROR)

class InventoryCreate(BaseModel):
    InstrumentID: int
    AccessoryID: int
    Quantity: int
    InventoryReceiptID: int | None

class InventoryData(InventoryCreate):
    InventoryID: int
    DateUpdated: str

class InventoryCRUD:
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
            logging.error(f"Database operation failed. {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during database operation"
            )

    def create(self, data: InventoryCreate):
        # Verificar que al menos uno de los IDs (InstrumentID o AccessoryID) esté presente
        if not data.InstrumentID and not data.AccessoryID:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide either an InstrumentID or AccessoryID"
            )

        # Elegir entre InstrumentID o AccessoryID
        instrument_id = data.InstrumentID if data.InstrumentID else None
        accessory_id = data.AccessoryID if data.AccessoryID else None

        query = """
            INSERT INTO Inventory (InstrumentID, AccessoryID, Quantity)
            VALUES (%s, %s, %s)
            RETURNING InventoryID;
        """
        try:
            values = (instrument_id, accessory_id, data.Quantity)
            cursor = self.db_connection.connection.cursor()
            cursor.execute(query, values)
            inventory_id = cursor.fetchone()[0]
            self.db_connection.connection.commit()
            cursor.close()
            return inventory_id
        except IntegrityError:
            self.db_connection.connection.rollback()
            logging.error("Integrity error while creating inventory.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error in inventory creation: Integrity error"
            )
        except Exception as e:
            logging.error(f"Error while creating inventory: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred while creating inventory"
            )

    def update(self, id_: int, data: InventoryData):
        query = """
            UPDATE Inventory
            SET InstrumentID = %s, AccessoryID = %s, Quantity = %s, InventoryReceiptID = %s
            WHERE InventoryID = %s;
        """
        values = (data.InstrumentID, data.AccessoryID, data.Quantity, data.InventoryReceiptID, id_)
        self._execution(query, values)

    def delete(self, id_: int):
        query = """
            DELETE FROM Inventory
            WHERE InventoryID = %s;
        """
        values = (id_,)
        self._execution(query, values)

    def get_by_id(self, id_: int) -> InventoryData:
        query = """
            SELECT InventoryID, InstrumentID, AccessoryID, Quantity, DateUpdated, InventoryReceiptID
            FROM Inventory
            WHERE InventoryID = %s;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query, (id_,))
        inventory = cursor.fetchone()
        cursor.close()
        if inventory:
            return InventoryData(
                InventoryID=inventory[0],
                InstrumentID=inventory[1],
                AccessoryID=inventory[2],
                Quantity=inventory[3],
                DateUpdated=str(inventory[4]),
                InventoryReceiptID=inventory[5]
            )
        raise HTTPException(status_code=404, detail="Inventory item not found")

    def get_all(self) -> List[InventoryData]:
        query = """
            SELECT I.InventoryID, 
                I.InstrumentID, 
                I.AccessoryID, 
                I.Quantity, 
                I.DateUpdated, 
                I.InventoryReceiptID
            FROM Inventory I
            ORDER BY I.DateUpdated DESC
            LIMIT 10 OFFSET 0;
        """
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        inventories = cursor.fetchall()
        cursor.close()
        
        if not inventories:
            raise HTTPException(status_code=404, detail="No inventory items found")
        
        return [
            InventoryData(
                InventoryID=row[0],
                InstrumentID=row[1],
                AccessoryID=row[2],
                Quantity=row[3],
                DateUpdated=str(row[4]),
                InventoryReceiptID=row[5]
            )
            for row in inventories
        ]

