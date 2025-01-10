import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from middleware.jwt_middleware import JWTMiddleware
from user_service.routes.users_routes import users_router
from user_service.routes.teams_routes import teams_router, teams_user_router
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ),
    Middleware(JWTMiddleware)
]

app = FastAPI(middleware=middleware)

app.include_router(users_router, prefix="/user", tags=["user"])
app.include_router(teams_router, prefix="/team", tags=["team"])
app.include_router(teams_user_router, prefix="/team", tags=["team_user"])