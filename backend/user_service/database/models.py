from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_group = Column(String(255), nullable=False, unique=True)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type_subscribe = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class TeamMember(Base):
    __tablename__ = 'team_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    table_args = (UniqueConstraint('team_id', 'user_id', name='_team_user_uc'),)
