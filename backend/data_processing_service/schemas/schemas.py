from pydantic import BaseModel
from typing import List

class Duration(BaseModel):
    nanos: int
    secs: int

class Time(BaseModel):
    nanos_since_epoch: int
    secs_since_epoch: int

class AFKMoment(BaseModel):
    duration: Duration
    start_time: Time

class LogEntry(BaseModel):
    afk_moments: List[AFKMoment]
    duration: Duration
    is_afk: bool
    name: str
    time: Time
    title: str

class LogRequest(BaseModel):
    log: List[LogEntry]

class LogResponse(BaseModel):
    log: List[LogEntry]
    username: str
    group: str