import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import FastAPI
from .routes import auth_router
from .routes import email_router
from .routes import users_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(email_router, prefix="/email", tags=["email"])