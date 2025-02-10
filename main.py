from fastapi import FastAPI, HTTPException
from typing import List
from CRUD.users import UserCRUD, UserData

app = FastAPI()
user_crud = UserCRUD()

@app.post("/users/", response_model=int)
def create_user(user: UserData):
    user_id = user_crud.create(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="Error creating user")
    return user_id

@app.get("/users/{user_id}", response_model=UserData)
def get_user(user_id: int):
    user = user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserData(UserID=user[0], Username=user[1], Password=user[2], Role=user[3], Email=user[4])

@app.get("/users/", response_model=List[UserData])
def get_all_users():
    users = user_crud.get_all()
    return [UserData(UserID=u[0], Username=u[1], Password=u[2], Role=u[3], Email=u[4]) for u in users]

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserData):
    if not user_crud.get_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.update(user_id, user)
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if not user_crud.get_by_id(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete(user_id)
    return {"message": "User deleted successfully"}
