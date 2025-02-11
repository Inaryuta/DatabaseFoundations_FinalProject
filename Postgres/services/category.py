from fastapi import APIRouter, HTTPException, status

from CRUD.category import categoryData, categoryCRUD

router = APIRouter()
crud = categoryCRUD()

@router.post("/category/create", response_model=int)
def create(data: categoryData):
    category_id = crud.create(data)
    if category_id is None:
        # Si la creación falló, se lanza una excepción HTTP
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating category"
        )
    return category_id

@router.put("/category/update/{id_}")
def update(id_: int, data: categoryData):
    return crud.update(id_, data)

@router.delete("/category/delete/{id_}")
def delete(id_: int):
    return crud.delete(id_)

@router.get("/category/get_by_id/{id_}")
def get_by_id(id_: int):
    return crud.get_by_id(id_)
@router.get("/category/get_all")
def get_all():
    return crud.get_all()

@router.get("/category/get_by_name/{name}")
def get_by_name(name: str):
    return crud.get_by_name(name)


@router.get("/category/get_by_email/{email}")
def get_by_email(email: str):
    return crud.get_by_email(email)