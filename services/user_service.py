from fastapi import APIRouter, HTTPException, status

from CRUD.user import UserData, userCRUD, UserCreate

router = APIRouter()
crud = userCRUD()

@router.post("/user/create", response_model=int)
def create(data: UserCreate):
    user_id = crud.create(data)
    if user_id is None:
        # Si la creación falló, se lanza una excepción HTTP
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user"
        )
    return user_id

@router.put("/user/update/{id_}")
def update(id_: int, data: UserData):
    return crud.update(id_, data)

@router.delete("/user/delete/{id_}")
def delete(id_: int):
    return crud.delete(id_)

@router.get("/user/get_by_id/{id_}")
def get_by_id(id_: int):
    return crud.get_by_id(id_)
@router.get("/user/get_all")
def get_all():
    return crud.get_all()

@router.get("/user/get_by_name/{name}")
def get_by_name(name: str):
    return crud.get_by_name(name)


@router.get("/user/get_by_email/{email}")
def get_by_email(email: str):
    return crud.get_by_email(email)