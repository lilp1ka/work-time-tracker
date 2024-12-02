from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import create_user, get_user, create_team, get_team
from database.schemas import UserCreate, UserResponse, TeamCreate, TeamResponse

from jose import JWTError, jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

router = APIRouter()

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/teams/", response_model=TeamResponse)
def create_team_route(team: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db=db, team=team)

@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team_route(team_id: int, db: Session = Depends(get_db)):
    team = get_team(db=db, team_id=team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/users/")
async def save_username(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split("Bearer ")[1]
    decoded_token = decode_jwt_token(token)

    username = decoded_token.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Username not found in token")

    user_data = UserCreate(username=username, is_active=True, is_admin=False)
    created_user = create_user(db=db, user=user_data)
    return {"status": "success", "user": created_user}