import time
from fastapi import Request, Depends, HTTPException
from database.database import collection
from schemas.schemas import LogRequest, LogResponse


class DataProcessing:
    def __init__(self):
        pass

    async def save_data(self, request: Request, log_request: LogRequest):
        username_from_jwt = await self.take_username_from_jwt(request)
        log_data = log_request.dict()
        log_data['username'] = username_from_jwt

        parsed_data = {
            "username": username_from_jwt,
            "time_save": time.time(),
            "logs": []
        }

        for entry in log_data['log']:
            parsed_entry = {
                "afk_moments": entry['afk_moments'],
                "duration": entry['duration'],
                "name": entry['name'],
                "time": entry['time'],
                "title": entry['title'],
            }
            parsed_data["logs"].append(parsed_entry)

        try:
            await collection.insert_one(parsed_data)
            return {"message": "Data saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")


    async def get_user_data(self, request: Request, username: str) -> LogResponse:
        username_from_jwt = await self.take_username_from_jwt(request)
        # в методе get_user_data мне нужно добавить фильты по дате
    async def get_group_data(self, request: Request, group: str) -> LogResponse:
        # метод в котором я получаю много юзернеймов и по ним нужно соснуть данные из бд
        pass

    @staticmethod
    async def take_username_from_jwt(request: Request):
        return request.state.user.get("username")


data_processing = DataProcessing()
