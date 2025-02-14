from fastapi import APIRouter
from CRUD.receipt import ReceiptCRUD, ReceiptCreate, ReceiptData


router = APIRouter()
crud = ReceiptCRUD()

@router.post("/receipt/create", response_model=int)
def create_receipt(data: ReceiptCreate):
    return crud.create(data)

@router.put("/receipt/update/{id_}")
def update_receipt(id_: int, data: ReceiptData):
    crud.update(id_, data)
    return {"message": "Receipt updated successfully"}

@router.delete("/receipt/delete/{id_}")
def delete_receipt(id_: int):
    return crud.delete(id_)

@router.get("/receipt/get_by_id/{id_}", response_model=ReceiptData)
def get_by_id_receipt(id_: int):
    return crud.get_by_id(id_)

@router.get("/receipt/get_all", response_model=list[ReceiptData])
def get_all_receipts():
    return crud.get_all()
