from fastapi import APIRouter
from CRUD.inventory import InventoryCRUD, InventoryCreate, InventoryData

router = APIRouter()
crud = InventoryCRUD()

@router.post("/inventory/create", response_model=int)
def create_inventory(data: InventoryCreate):
    return crud.create(data)

@router.put("/inventory/update/{id_}")
def update_inventory(id_: int, data: InventoryData):
    return crud.update(id_, data)

@router.delete("/inventory/delete/{id_}")
def delete_inventory(id_: int):
    return crud.delete(id_)

@router.get("/inventory/get_by_id/{id_}", response_model=InventoryData)
def get_by_id_inventory(id_: int):
    return crud.get_by_id(id_)

@router.get("/inventory/get_all", response_model=list[InventoryData])
def get_all_inventories():
    return crud.get_all()
