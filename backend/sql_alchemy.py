import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships
session_speaker = Table(
    "session_speaker",
    Base.metadata,
    Column("session", ForeignKey("session.id"), primary_key=True),
    Column("speaker", ForeignKey("speaker.id"), primary_key=True),
)

# Tables definition
class Speaker(Base):
    __tablename__ = "speaker"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullName: Mapped[str] = mapped_column(String(100))
    affiliation: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))

class ScheduleSlot(Base):
    __tablename__ = "scheduleslot"
    id: Mapped[int] = mapped_column(primary_key=True)
    startTime: Mapped[dt_datetime] = mapped_column(DateTime)
    endTime: Mapped[dt_datetime] = mapped_column(DateTime)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"), unique=True)

class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    capacity: Mapped[int] = mapped_column(Integer)

class Session(Base):
    __tablename__ = "session"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    sessionType: Mapped[str] = mapped_column(String(100))
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))

class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    startDate: Mapped[dt_date] = mapped_column(Date)
    location: Mapped[str] = mapped_column(String(100))
    endDate: Mapped[dt_date] = mapped_column(Date)


#--- Relationships of the speaker table
Speaker.session: Mapped[List["Session"]] = relationship("Session", secondary=session_speaker, back_populates="speaker")

#--- Relationships of the scheduleslot table
ScheduleSlot.session: Mapped["Session"] = relationship("Session", back_populates="scheduleSlot", foreign_keys=[ScheduleSlot.session_id])

#--- Relationships of the room table
Room.session: Mapped[List["Session"]] = relationship("Session", back_populates="room", foreign_keys=[Session.room_id])

#--- Relationships of the session table
Session.speaker: Mapped[List["Speaker"]] = relationship("Speaker", secondary=session_speaker, back_populates="session")
Session.event: Mapped["Event"] = relationship("Event", back_populates="session", foreign_keys=[Session.event_id])
Session.room: Mapped["Room"] = relationship("Room", back_populates="session", foreign_keys=[Session.room_id])
Session.scheduleSlot: Mapped["ScheduleSlot"] = relationship("ScheduleSlot", back_populates="session", foreign_keys=[ScheduleSlot.session_id])

#--- Relationships of the event table
Event.session: Mapped[List["Session"]] = relationship("Session", back_populates="event", foreign_keys=[Session.event_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)