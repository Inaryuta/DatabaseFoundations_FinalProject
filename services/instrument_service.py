from fastapi import APIRouter
from CRUD.instrument import InstrumentCRUD, InstrumentCreate, InstrumentData

router = APIRouter()
crud = InstrumentCRUD()

@router.post("/instrument/create", response_model=int)
def create_instrument(data: InstrumentCreate):
    return crud.create(data)

@router.put("/instrument/update/{id_}")
def update_instrument(id_: int, data: InstrumentData):
    return crud.update(id_, data)

@router.delete("/instrument/delete/{id_}")
def delete_instrument(id_: int):
    return crud.delete(id_)

@router.get("/instrument/get_by_id/{id_}", response_model=InstrumentData)
def get_by_id_instrument(id_: int):
    return crud.get_by_id(id_)

@router.get("/instrument/get_all", response_model=list[InstrumentData])
def get_all_instruments():
    return crud.get_all()
