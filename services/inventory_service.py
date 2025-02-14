from fastapi import APIRouter
from CRUD.inventory import InventoryCRUD, InventoryCreate, InventoryData
from fastapi.responses import JSONResponse
from fastapi import HTTPException

router = APIRouter()
crud = InventoryCRUD()

@router.post("/inventory/create", response_model=int)
def create_inventory(data: InventoryCreate):
    try:
        inventory_id = crud.create(data)
        return JSONResponse(status_code=201, content={"InventoryID": inventory_id})
    except HTTPException as e:
        raise e  # Re-raise the HTTP exception to be caught by FastAPI's error handler
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the inventory"
        )

@router.put("/inventory/update/{id_}")
def update_inventory(id_: int, data: InventoryData):
    try:
        crud.update(id_, data)
        return {"message": "Inventory updated successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the inventory"
        )

@router.delete("/inventory/delete/{id_}")
def delete_inventory(id_: int):
    try:
        crud.delete(id_)
        return {"message": "Inventory deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the inventory"
        )

@router.get("/inventory/get_by_id/{id_}", response_model=InventoryData)
def get_by_id_inventory(id_: int):
    try:
        return crud.get_by_id(id_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the inventory"
        )

@router.get("/inventory/get_all", response_model=list[InventoryData])
def get_all_inventories():
    try:
        return crud.get_all()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving inventory items"
        )
