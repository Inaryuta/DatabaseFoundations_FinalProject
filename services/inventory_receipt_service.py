from fastapi import APIRouter, HTTPException, status
from CRUD.inventory_receipt import InventoryReceiptData, inventoryReceiptCRUD, InventoryReceiptCreate

router = APIRouter()
crud = inventoryReceiptCRUD()

@router.post("/inventory_receipt/create", response_model=int)
def create(data: InventoryReceiptCreate):
    inventory_receipt_id = crud.create(data)
    if inventory_receipt_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating inventory receipt"
        )
    return inventory_receipt_id

@router.put("/inventory_receipt/update/{id_}")
def update(id_: int, data: InventoryReceiptData):
    return crud.update(id_, data)

@router.delete("/inventory_receipt/delete/{id_}")
def delete(id_: int):
    return crud.delete(id_)

@router.get("/inventory_receipt/get_by_id/{id_}")
def get_by_id(id_: int):
    return crud.get_by_id(id_)

@router.get("/inventory_receipt/get_all")
def get_all():
    return crud.get_all()
