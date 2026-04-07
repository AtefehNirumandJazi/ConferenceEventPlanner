from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator

from abc import ABC, abstractmethod

############################################
# Enumerations are defined here
############################################

############################################
# Classes are defined here
############################################
class SpeakerCreate(BaseModel):
    email: str
    fullName: str
    affiliation: str
    session: List[int]  # N:M Relationship


class ScheduleSlotCreate(BaseModel):
    endTime: datetime
    startTime: datetime
    session: int  # 1:1 Relationship (mandatory)


class RoomCreate(BaseModel):
    capacity: int
    name: str
    session: Optional[List[int]] = None  # 1:N Relationship


class SessionCreate(ABC, BaseModel):
    description: str
    sessionType: str
    title: str
    scheduleSlot: Optional[int] = None  # 1:1 Relationship (optional)
    speaker: Optional[List[int]] = None  # N:M Relationship (optional)
    event: int  # N:1 Relationship (mandatory)
    room: int  # N:1 Relationship (mandatory)


class EventCreate(BaseModel):
    name: str
    location: str
    startDate: date
    endDate: date
    session: Optional[List[int]] = None  # 1:N Relationship


