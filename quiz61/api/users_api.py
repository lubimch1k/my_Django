from fastapi import APIRouter
from database.userservice import *
from database.questionservice import *

user_router = APIRouter(prefix="/user",
                        tags=["ПОЛЬЗОВАТЕЛЬСКАЯ ЧАСТЬ"])
@user_router.post("/login")
async def login_register(username: str, phone_number: str):
    result = add_user_db(username, phone_number)
    if result:
        return {"status": 1, "message": result}
    return {"status": 0, "message": "Не удалось войти"}
