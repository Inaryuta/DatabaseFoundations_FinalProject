from fastapi import APIRouter
from CRUD.supplier import SupplierCRUD, SupplierCreate, SupplierData

router = APIRouter()
crud = SupplierCRUD()

@router.post("/supplier/create", response_model=int)
def create_supplier(data: SupplierCreate):
    return crud.create(data)

@router.put("/supplier/update/{id_}")
def update_supplier(id_: int, data: SupplierData):
    return crud.update(id_, data)

@router.delete("/supplier/delete/{id_}")
def delete_supplier(id_: int):
    return crud.delete(id_)

@router.get("/supplier/get_by_id/{id_}", response_model=SupplierData)
def get_by_id_supplier(id_: int):
    return crud.get_by_id(id_)

@router.get("/supplier/get_all", response_model=list[SupplierData])
def get_all_suppliers():
    return crud.get_all()
