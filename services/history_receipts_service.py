from fastapi import APIRouter
from CRUD.history_receipts import HistoryReceiptsCRUD, HistoryReceiptsCreate, HistoryReceiptsData

router = APIRouter()
crud = HistoryReceiptsCRUD()

@router.post("/history_receipts/create", response_model=int)
def create_history_receipt(data: HistoryReceiptsCreate):
    return crud.create(data)

@router.put("/history_receipts/update/{id_}")
def update_history_receipt(id_: int, data: HistoryReceiptsCreate):
    return crud.update(id_, data)

@router.delete("/history_receipts/delete/{id_}")
def delete_history_receipt(id_: int):
    return crud.delete(id_)

@router.get("/history_receipts/get_by_id/{id_}", response_model=HistoryReceiptsData)
def get_by_id_history_receipt(id_: int):
    return crud.get_by_id(id_)

@router.get("/history_receipts/get_all", response_model=list[HistoryReceiptsData])
def get_all_history_receipts():
    return crud.get_all()
