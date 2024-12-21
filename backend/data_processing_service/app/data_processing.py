from fastapi import Request, Depends
from database.database import collection
from schemas.schemas import LogRequest


class DataProcessing:
    def __init__(self):
        pass

    async def save_data(self, request: Request, log: LogRequest = Depends()):
        username = request.state.user.get("username")
        


data_processing = DataProcessing()