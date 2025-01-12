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

    async def get_user_data(self, request: Request, username: str, date_from: str = None,
                            date_to: str = None) -> LogResponse:
        query = {"username": username}
        if date_from:
            query["time_save"] = {"$gte": date_from}
        if date_to:
            if "time_save" in query:
                query["time_save"]["$lte"] = date_to
            else:
                query["time_save"] = {"$lte": date_to}

        try:
            user_data = await collection.find(query).to_list(length=None)
            if not user_data:
                raise HTTPException(status_code=404, detail="User data not found")
            return LogResponse(data=user_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving user data: {str(e)}")

    async def get_group_data(self, request: Request, group: str, usernames: list, date_from: str = None,
                                 date_to: str = None) -> LogResponse:
        user_data_list = []

        for username in usernames:
            user_data = await self.get_user_data(request, username, date_from, date_to)
            user_data_list.append(user_data.data)
        return LogResponse(data=user_data_list)

    @staticmethod
    async def take_username_from_jwt(request: Request):
        return request.state.user


data_processing = DataProcessing()