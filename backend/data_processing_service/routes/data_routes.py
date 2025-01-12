# принять данные от лешки
# сохранить + распарсить в человеческий вид + отправить в редис и когда будет N записей ебануть в бд
#
# отправить ВСЮ статистику одного юзера \ за определенное дату либо промежуток даты (день неделя месяц)
# отправить статистику по всем юзерам определенной группы \ за определенное дату либо промежуток даты (день неделя месяц)

from fastapi import APIRouter, Request, Depends
from app.data_processing import data_processing
from schemas.schemas import LogRequest, LogResponse

data_router = APIRouter()

@data_router.post("/save_data")
async def save_data(request: Request, log_request: LogRequest):
    return await data_processing.save_data(request, log_request)


@data_router.get("/get_user_data", response_model=LogResponse)
async def get_user_data(request: Request, username: str, date_from: str = None, date_to: str = None):
    return await data_processing.get_user_data(request, username, date_from, date_to)


@data_router.get("/get_group_data", response_model=LogResponse)
async def get_group_data(request: Request, group: str, usernames: list, date_from: str = None, date_to: str = None):
    return await data_processing.get_group_data(request, group, usernames, date_from, date_to)
