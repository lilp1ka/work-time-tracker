from sqlalchemy.orm import Session
from .models import User, Team
from .schemas import UserCreate, TeamCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, is_active=user.is_active, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_team(db: Session, team: TeamCreate):
    db_team = Team(name_group=team.name_group, creator_id=team.creator_id, admin_id=team.admin_id, type_subscribe=team.type_subscribe)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_team(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()
