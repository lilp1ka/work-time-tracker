from routes import users_router as router


class ChangeUserData:
    def __init__(self):
        self.router = router

    async def change_password(self):
        pass

    async def change_email(self):
        pass

    async def change_username(self):
        pass

    async def reset_password(self):
        pass

    async def delete_user(self):
        pass

class UserData:
    def __init__(self):
        self.router = router

    async def get_user(self):
        pass

    async def get_all_users(self):
        pass

    async def get_user_by_username(self):
        pass

    async def get_user_by_id(self):
        pass