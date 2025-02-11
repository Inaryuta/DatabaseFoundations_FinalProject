from fastapi import APIRouter
from CRUD.accessory import AccessoryCRUD, AccessoryCreate, AccessoryData

router = APIRouter()
crud = AccessoryCRUD()

@router.post("/accessory/create", response_model=int)
def create_accessory(data: AccessoryCreate):
    return crud.create(data)

@router.put("/accessory/update/{id_}")
def update_accessory(id_: int, data: AccessoryData):
    return crud.update(id_, data)

@router.delete("/accessory/delete/{id_}")
def delete_accessory(id_: int):
    return crud.delete(id_)

@router.get("/accessory/get_by_id/{id_}", response_model=AccessoryData)
def get_by_id_accessory(id_: int):
    return crud.get_by_id(id_)

@router.get("/accessory/get_all", response_model=list[AccessoryData])
def get_all_accessories():
    return crud.get_all()
