from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.crud import create_user, get_user, create_team, get_team
from database.schemas import UserCreate, UserResponse, TeamCreate, TeamResponse

router = APIRouter()

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
