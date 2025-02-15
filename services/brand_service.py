from fastapi import APIRouter, HTTPException, status
from CRUD.brand import BrandData, BrandCRUD, BrandCreate

router = APIRouter()
crud = BrandCRUD()

@router.post("/brand/create", response_model=int)
def create(data: BrandCreate):
    brand_id = crud.create(data)
    if brand_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating brand"
        )
    return brand_id

@router.put("/brand/update/{id_}")
def update(id_: int, data: BrandData):
    return crud.update(id_, data)

@router.delete("/brand/delete/{id_}")
def delete(id_: int):
    return crud.delete(id_)

@router.get("/brand/get_by_id/{id_}")
def get_by_id(id_: int):
    return crud.get_by_id(id_)

@router.get("/brand/get_all")
def get_all():
    return crud.get_all()

@router.get("/brand/get_by_name/{name}")
def get_by_name(name: str):
    return crud.get_by_name(name)
