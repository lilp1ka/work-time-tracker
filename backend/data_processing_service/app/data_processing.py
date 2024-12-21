from fastapi import Request, Depends, HTTPException
from database.database import collection
from schemas.schemas import LogRequest, LogResponse


class DataProcessing:
    def __init__(self):
        pass

    async def save_data(self, request: Request, log: LogRequest = Depends()):
        username_from_jwt = await self.take_username_from_jwt(request)
        log_data = log.dict()
        log_data['username'] = username_from_jwt
        await collection.insert_one(log_data)
        return {"message": "Data saved successfully"}

    async def get_user_data(self, request: Request, username: str) -> LogResponse:
        username_from_jwt = await self.take_username_from_jwt(request)
        if username_from_jwt != username:
            raise HTTPException(status_code=403, detail="Forbidden")
        logs = await collection.find({"username": username}).to_list(length=None)
        return LogResponse(log=logs, username=username, group="")

    async def get_group_data(self, request: Request, group: str) -> LogResponse:
        group_from_jwt = await self.take_group_from_jwt(request)
        if group_from_jwt != group:
            raise HTTPException(status_code=403, detail="Forbidden")
        logs = await collection.find({"group": group}).to_list(length=None)
        return LogResponse(log=logs, username="", group=group)

    @staticmethod
    async def take_username_from_jwt(request: Request):
        return request.state.user.get("username")

    @staticmethod
    async def take_group_from_jwt(request: Request):
        return request.state.user.get("group")

data_processing = DataProcessing()
