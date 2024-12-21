# принять данные от лешки
# сохранить + распарсить в человеческий вид + отправить в редис и когда будет N записей ебануть в бд
#
# отправить ВСЮ статистику одного юзера \ за определенное дату либо промежуток даты (день неделя месяц)
# отправить статистику по всем юзерам определенной группы \ за определенное дату либо промежуток даты (день неделя месяц)

from fastapi import APIRouter, Request
from app.data_processing import data_processing

data_router = APIRouter()

@data_router.post("/save_data")
async def save_data(request: Request):
    return await data_processing.save_data(request)

@data_router.get("/get_user_data")
async def get_user_data():
    pass

@data_router.get("/get_group_data")
async def get_group_data():
    pass
