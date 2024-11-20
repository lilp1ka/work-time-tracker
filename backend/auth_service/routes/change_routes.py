from fastapi import APIRouter
from auth_service.app.user_data import change_user_instance

change_router = APIRouter()


@change_router.patch("/change-password")
async def change_password():
    pass


@change_router.delete("/delete-user")
async def delete_user():
    pass


@change_router.patch("/change-email")
async def change_email():
    pass


@change_router.patch("/change-username")
async def change_username():
    pass


@change_router.patch("/reset-password")
async def reset_password():
    pass
