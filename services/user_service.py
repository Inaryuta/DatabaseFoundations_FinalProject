from fastapi import APIRouter, HTTPException, status
from CRUD.user import UserData, userCRUD, UserCreate

router = APIRouter()
crud = userCRUD()

@router.post("/user/create", response_model=UserData)
def create(data: UserCreate):
    try:
        user = crud.create(data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")

@router.put("/user/update/{id_}")
def update(id_: int, data: UserData):
    try:
        return crud.update(id_, data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating user")

@router.delete("/user/delete/{id_}")
def delete(id_: int):
    try:
        return crud.delete(id_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error deleting user")

@router.get("/user/get_by_id/{id_}")
def get_by_id(id_: int):
    try:
        return crud.get_by_id(id_)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error fetching user")

@router.get("/user/get_all")
def get_all():
    try:
        return crud.get_all()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error fetching all users")

@router.get("/user/get_by_name/{name}")
def get_by_name(name: str):
    try:
        return crud.get_by_name(name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error fetching users by name")

@router.get("/user/get_by_email/{email}")
def get_by_email(email: str):
    try:
        return crud.get_by_email(email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error fetching user by email")
