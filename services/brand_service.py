from fastapi import APIRouter, HTTPException, status
from typing import List
from CRUD.brand import BrandCRUD, BrandCreate, BrandData

router = APIRouter()
crud = BrandCRUD()

@router.post("/brand/create", response_model=BrandData)
def create(data: BrandCreate):
    return crud.create(data)

@router.get("/brand/get_all", response_model=List[BrandData])
def get_all(limit: int = 50, offset: int = 0):
    return crud.get_all(limit, offset)

@router.get("/brand/get/{id_}", response_model=BrandData)
def get_by_id(id_: int):
    return crud.get_by_id(id_)

@router.put("/brand/update/{id_}")
def update(id_: int, data: BrandCreate):
    return crud.update(id_, data)

@router.delete("/brand/delete/{id_}")
def delete(id_: int):
    return crud.delete(id_)

@router.get("/brand/get_by_name/{name}", response_model=List[BrandData])
def get_by_name(name: str):
    return crud.get_by_name(name)

@router.get("/brand/get_by_country/{country}", response_model=List[BrandData])
def get_by_country(country: str):
    return crud.get_by_country(country)
