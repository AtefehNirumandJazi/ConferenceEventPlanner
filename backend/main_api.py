import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Speaker", "description": "Operations for Speaker entities"},
        {"name": "Speaker Relationships", "description": "Manage Speaker relationships"},
        {"name": "ScheduleSlot", "description": "Operations for ScheduleSlot entities"},
        {"name": "ScheduleSlot Relationships", "description": "Manage ScheduleSlot relationships"},
        {"name": "Room", "description": "Operations for Room entities"},
        {"name": "Room Relationships", "description": "Manage Room relationships"},
        {"name": "Session", "description": "Operations for Session entities"},
        {"name": "Session Relationships", "description": "Manage Session relationships"},
        {"name": "Event", "description": "Operations for Event entities"},
        {"name": "Event Relationships", "description": "Manage Event relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["speaker_count"] = database.query(Speaker).count()
    stats["scheduleslot_count"] = database.query(ScheduleSlot).count()
    stats["room_count"] = database.query(Room).count()
    stats["session_count"] = database.query(Session).count()
    stats["event_count"] = database.query(Event).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Speaker functions
#
############################################

@app.get("/speaker/", response_model=None, tags=["Speaker"])
def get_all_speaker(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Speaker)
        speaker_list = query.all()

        # Serialize with relationships included
        result = []
        for speaker_item in speaker_list:
            item_dict = speaker_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            session_list = database.query(Session).join(session_speaker, Session.id == session_speaker.c.session).filter(session_speaker.c.speaker == speaker_item.id).all()
            item_dict['session'] = []
            for session_obj in session_list:
                session_dict = session_obj.__dict__.copy()
                session_dict.pop('_sa_instance_state', None)
                item_dict['session'].append(session_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Speaker).all()


@app.get("/speaker/count/", response_model=None, tags=["Speaker"])
def get_count_speaker(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Speaker entities"""
    count = database.query(Speaker).count()
    return {"count": count}


@app.get("/speaker/paginated/", response_model=None, tags=["Speaker"])
def get_paginated_speaker(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Speaker entities"""
    total = database.query(Speaker).count()
    speaker_list = database.query(Speaker).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": speaker_list
        }

    result = []
    for speaker_item in speaker_list:
        session_ids = database.query(session_speaker.c.session).filter(session_speaker.c.speaker == speaker_item.id).all()
        item_data = {
            "speaker": speaker_item,
            "session_ids": [x[0] for x in session_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/speaker/search/", response_model=None, tags=["Speaker"])
def search_speaker(
    database: Session = Depends(get_db)
) -> list:
    """Search Speaker entities by attributes"""
    query = database.query(Speaker)


    results = query.all()
    return results


@app.get("/speaker/{speaker_id}/", response_model=None, tags=["Speaker"])
async def get_speaker(speaker_id: int, database: Session = Depends(get_db)) -> Speaker:
    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")

    session_ids = database.query(session_speaker.c.session).filter(session_speaker.c.speaker == db_speaker.id).all()
    response_data = {
        "speaker": db_speaker,
        "session_ids": [x[0] for x in session_ids],
}
    return response_data



@app.post("/speaker/", response_model=None, tags=["Speaker"])
async def create_speaker(speaker_data: SpeakerCreate, database: Session = Depends(get_db)) -> Speaker:

    if not speaker_data.session or len(speaker_data.session) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Session(s) required")
    if speaker_data.session:
        for id in speaker_data.session:
            # Entity already validated before creation
            db_session = database.query(Session).filter(Session.id == id).first()
            if not db_session:
                raise HTTPException(status_code=404, detail=f"Session with ID {id} not found")

    db_speaker = Speaker(
        email=speaker_data.email,        fullName=speaker_data.fullName,        affiliation=speaker_data.affiliation        )

    database.add(db_speaker)
    database.commit()
    database.refresh(db_speaker)


    if speaker_data.session:
        for id in speaker_data.session:
            # Entity already validated before creation
            db_session = database.query(Session).filter(Session.id == id).first()
            # Create the association
            association = session_speaker.insert().values(speaker=db_speaker.id, session=db_session.id)
            database.execute(association)
            database.commit()


    session_ids = database.query(session_speaker.c.session).filter(session_speaker.c.speaker == db_speaker.id).all()
    response_data = {
        "speaker": db_speaker,
        "session_ids": [x[0] for x in session_ids],
    }
    return response_data


@app.post("/speaker/bulk/", response_model=None, tags=["Speaker"])
async def bulk_create_speaker(items: list[SpeakerCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Speaker entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_speaker = Speaker(
                email=item_data.email,                fullName=item_data.fullName,                affiliation=item_data.affiliation            )
            database.add(db_speaker)
            database.flush()  # Get ID without committing
            created_items.append(db_speaker.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Speaker entities"
    }


@app.delete("/speaker/bulk/", response_model=None, tags=["Speaker"])
async def bulk_delete_speaker(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Speaker entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_speaker = database.query(Speaker).filter(Speaker.id == item_id).first()
        if db_speaker:
            database.delete(db_speaker)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Speaker entities"
    }

@app.put("/speaker/{speaker_id}/", response_model=None, tags=["Speaker"])
async def update_speaker(speaker_id: int, speaker_data: SpeakerCreate, database: Session = Depends(get_db)) -> Speaker:
    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")

    setattr(db_speaker, 'email', speaker_data.email)
    setattr(db_speaker, 'fullName', speaker_data.fullName)
    setattr(db_speaker, 'affiliation', speaker_data.affiliation)
    existing_session_ids = [assoc.session for assoc in database.execute(
        session_speaker.select().where(session_speaker.c.speaker == db_speaker.id))]

    sessions_to_remove = set(existing_session_ids) - set(speaker_data.session)
    for session_id in sessions_to_remove:
        association = session_speaker.delete().where(
            (session_speaker.c.speaker == db_speaker.id) & (session_speaker.c.session == session_id))
        database.execute(association)

    new_session_ids = set(speaker_data.session) - set(existing_session_ids)
    for session_id in new_session_ids:
        db_session = database.query(Session).filter(Session.id == session_id).first()
        if db_session is None:
            raise HTTPException(status_code=404, detail=f"Session with ID {session_id} not found")
        association = session_speaker.insert().values(session=db_session.id, speaker=db_speaker.id)
        database.execute(association)
    database.commit()
    database.refresh(db_speaker)

    session_ids = database.query(session_speaker.c.session).filter(session_speaker.c.speaker == db_speaker.id).all()
    response_data = {
        "speaker": db_speaker,
        "session_ids": [x[0] for x in session_ids],
    }
    return response_data


@app.delete("/speaker/{speaker_id}/", response_model=None, tags=["Speaker"])
async def delete_speaker(speaker_id: int, database: Session = Depends(get_db)):
    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")
    database.delete(db_speaker)
    database.commit()
    return db_speaker

@app.post("/speaker/{speaker_id}/session/{session_id}/", response_model=None, tags=["Speaker Relationships"])
async def add_session_to_speaker(speaker_id: int, session_id: int, database: Session = Depends(get_db)):
    """Add a Session to this Speaker's session relationship"""
    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")

    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if relationship already exists
    existing = database.query(session_speaker).filter(
        (session_speaker.c.speaker == speaker_id) &
        (session_speaker.c.session == session_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = session_speaker.insert().values(speaker=speaker_id, session=session_id)
    database.execute(association)
    database.commit()

    return {"message": "Session added to session successfully"}


@app.delete("/speaker/{speaker_id}/session/{session_id}/", response_model=None, tags=["Speaker Relationships"])
async def remove_session_from_speaker(speaker_id: int, session_id: int, database: Session = Depends(get_db)):
    """Remove a Session from this Speaker's session relationship"""
    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")

    # Check if relationship exists
    existing = database.query(session_speaker).filter(
        (session_speaker.c.speaker == speaker_id) &
        (session_speaker.c.session == session_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = session_speaker.delete().where(
        (session_speaker.c.speaker == speaker_id) &
        (session_speaker.c.session == session_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Session removed from session successfully"}


@app.get("/speaker/{speaker_id}/session/", response_model=None, tags=["Speaker Relationships"])
async def get_session_of_speaker(speaker_id: int, database: Session = Depends(get_db)):
    """Get all Session entities related to this Speaker through session"""
    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")

    session_ids = database.query(session_speaker.c.session).filter(session_speaker.c.speaker == speaker_id).all()
    session_list = database.query(Session).filter(Session.id.in_([id[0] for id in session_ids])).all()

    return {
        "speaker_id": speaker_id,
        "session_count": len(session_list),
        "session": session_list
    }





############################################
#
#   ScheduleSlot functions
#
############################################

@app.get("/scheduleslot/", response_model=None, tags=["ScheduleSlot"])
def get_all_scheduleslot(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ScheduleSlot)
        query = query.options(joinedload(ScheduleSlot.session))
        scheduleslot_list = query.all()

        # Serialize with relationships included
        result = []
        for scheduleslot_item in scheduleslot_list:
            item_dict = scheduleslot_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if scheduleslot_item.session:
                related_obj = scheduleslot_item.session
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['session'] = related_dict
            else:
                item_dict['session'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ScheduleSlot).all()


@app.get("/scheduleslot/count/", response_model=None, tags=["ScheduleSlot"])
def get_count_scheduleslot(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ScheduleSlot entities"""
    count = database.query(ScheduleSlot).count()
    return {"count": count}


@app.get("/scheduleslot/paginated/", response_model=None, tags=["ScheduleSlot"])
def get_paginated_scheduleslot(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ScheduleSlot entities"""
    total = database.query(ScheduleSlot).count()
    scheduleslot_list = database.query(ScheduleSlot).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": scheduleslot_list
    }


@app.get("/scheduleslot/search/", response_model=None, tags=["ScheduleSlot"])
def search_scheduleslot(
    database: Session = Depends(get_db)
) -> list:
    """Search ScheduleSlot entities by attributes"""
    query = database.query(ScheduleSlot)


    results = query.all()
    return results


@app.get("/scheduleslot/{scheduleslot_id}/", response_model=None, tags=["ScheduleSlot"])
async def get_scheduleslot(scheduleslot_id: int, database: Session = Depends(get_db)) -> ScheduleSlot:
    db_scheduleslot = database.query(ScheduleSlot).filter(ScheduleSlot.id == scheduleslot_id).first()
    if db_scheduleslot is None:
        raise HTTPException(status_code=404, detail="ScheduleSlot not found")

    response_data = {
        "scheduleslot": db_scheduleslot,
}
    return response_data



@app.post("/scheduleslot/", response_model=None, tags=["ScheduleSlot"])
async def create_scheduleslot(scheduleslot_data: ScheduleSlotCreate, database: Session = Depends(get_db)) -> ScheduleSlot:

    if scheduleslot_data.session is not None:
        db_session = database.query(Session).filter(Session.id == scheduleslot_data.session).first()
        if not db_session:
            raise HTTPException(status_code=400, detail="Session not found")
    else:
        raise HTTPException(status_code=400, detail="Session ID is required")

    db_scheduleslot = ScheduleSlot(
        endTime=scheduleslot_data.endTime,        startTime=scheduleslot_data.startTime,        session_id=scheduleslot_data.session        )

    database.add(db_scheduleslot)
    database.commit()
    database.refresh(db_scheduleslot)




    return db_scheduleslot


@app.post("/scheduleslot/bulk/", response_model=None, tags=["ScheduleSlot"])
async def bulk_create_scheduleslot(items: list[ScheduleSlotCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ScheduleSlot entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.session:
                raise ValueError("Session ID is required")

            db_scheduleslot = ScheduleSlot(
                endTime=item_data.endTime,                startTime=item_data.startTime,                session_id=item_data.session            )
            database.add(db_scheduleslot)
            database.flush()  # Get ID without committing
            created_items.append(db_scheduleslot.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ScheduleSlot entities"
    }


@app.delete("/scheduleslot/bulk/", response_model=None, tags=["ScheduleSlot"])
async def bulk_delete_scheduleslot(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ScheduleSlot entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_scheduleslot = database.query(ScheduleSlot).filter(ScheduleSlot.id == item_id).first()
        if db_scheduleslot:
            database.delete(db_scheduleslot)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ScheduleSlot entities"
    }

@app.put("/scheduleslot/{scheduleslot_id}/", response_model=None, tags=["ScheduleSlot"])
async def update_scheduleslot(scheduleslot_id: int, scheduleslot_data: ScheduleSlotCreate, database: Session = Depends(get_db)) -> ScheduleSlot:
    db_scheduleslot = database.query(ScheduleSlot).filter(ScheduleSlot.id == scheduleslot_id).first()
    if db_scheduleslot is None:
        raise HTTPException(status_code=404, detail="ScheduleSlot not found")

    setattr(db_scheduleslot, 'endTime', scheduleslot_data.endTime)
    setattr(db_scheduleslot, 'startTime', scheduleslot_data.startTime)
    if scheduleslot_data.session is not None:
        db_session = database.query(Session).filter(Session.id == scheduleslot_data.session).first()
        if not db_session:
            raise HTTPException(status_code=400, detail="Session not found")
        setattr(db_scheduleslot, 'session_id', scheduleslot_data.session)
    database.commit()
    database.refresh(db_scheduleslot)

    return db_scheduleslot


@app.delete("/scheduleslot/{scheduleslot_id}/", response_model=None, tags=["ScheduleSlot"])
async def delete_scheduleslot(scheduleslot_id: int, database: Session = Depends(get_db)):
    db_scheduleslot = database.query(ScheduleSlot).filter(ScheduleSlot.id == scheduleslot_id).first()
    if db_scheduleslot is None:
        raise HTTPException(status_code=404, detail="ScheduleSlot not found")
    database.delete(db_scheduleslot)
    database.commit()
    return db_scheduleslot





############################################
#
#   Room functions
#
############################################

@app.get("/room/", response_model=None, tags=["Room"])
def get_all_room(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Room)
        room_list = query.all()

        # Serialize with relationships included
        result = []
        for room_item in room_list:
            item_dict = room_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            session_list = database.query(Session).filter(Session.room_id == room_item.id).all()
            item_dict['session'] = []
            for session_obj in session_list:
                session_dict = session_obj.__dict__.copy()
                session_dict.pop('_sa_instance_state', None)
                item_dict['session'].append(session_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Room).all()


@app.get("/room/count/", response_model=None, tags=["Room"])
def get_count_room(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Room entities"""
    count = database.query(Room).count()
    return {"count": count}


@app.get("/room/paginated/", response_model=None, tags=["Room"])
def get_paginated_room(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Room entities"""
    total = database.query(Room).count()
    room_list = database.query(Room).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": room_list
        }

    result = []
    for room_item in room_list:
        session_ids = database.query(Session.id).filter(Session.room_id == room_item.id).all()
        item_data = {
            "room": room_item,
            "session_ids": [x[0] for x in session_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/room/search/", response_model=None, tags=["Room"])
def search_room(
    database: Session = Depends(get_db)
) -> list:
    """Search Room entities by attributes"""
    query = database.query(Room)


    results = query.all()
    return results


@app.get("/room/{room_id}/", response_model=None, tags=["Room"])
async def get_room(room_id: int, database: Session = Depends(get_db)) -> Room:
    db_room = database.query(Room).filter(Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    session_ids = database.query(Session.id).filter(Session.room_id == db_room.id).all()
    response_data = {
        "room": db_room,
        "session_ids": [x[0] for x in session_ids]}
    return response_data



@app.post("/room/", response_model=None, tags=["Room"])
async def create_room(room_data: RoomCreate, database: Session = Depends(get_db)) -> Room:


    db_room = Room(
        capacity=room_data.capacity,        name=room_data.name        )

    database.add(db_room)
    database.commit()
    database.refresh(db_room)

    if room_data.session:
        # Validate that all Session IDs exist
        for session_id in room_data.session:
            db_session = database.query(Session).filter(Session.id == session_id).first()
            if not db_session:
                raise HTTPException(status_code=400, detail=f"Session with id {session_id} not found")

        # Update the related entities with the new foreign key
        database.query(Session).filter(Session.id.in_(room_data.session)).update(
            {Session.room_id: db_room.id}, synchronize_session=False
        )
        database.commit()



    session_ids = database.query(Session.id).filter(Session.room_id == db_room.id).all()
    response_data = {
        "room": db_room,
        "session_ids": [x[0] for x in session_ids]    }
    return response_data


@app.post("/room/bulk/", response_model=None, tags=["Room"])
async def bulk_create_room(items: list[RoomCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Room entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_room = Room(
                capacity=item_data.capacity,                name=item_data.name            )
            database.add(db_room)
            database.flush()  # Get ID without committing
            created_items.append(db_room.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Room entities"
    }


@app.delete("/room/bulk/", response_model=None, tags=["Room"])
async def bulk_delete_room(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Room entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_room = database.query(Room).filter(Room.id == item_id).first()
        if db_room:
            database.delete(db_room)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Room entities"
    }

@app.put("/room/{room_id}/", response_model=None, tags=["Room"])
async def update_room(room_id: int, room_data: RoomCreate, database: Session = Depends(get_db)) -> Room:
    db_room = database.query(Room).filter(Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    setattr(db_room, 'capacity', room_data.capacity)
    setattr(db_room, 'name', room_data.name)
    if room_data.session is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Session).filter(Session.room_id == db_room.id).update(
            {Session.room_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if room_data.session:
            # Validate that all IDs exist
            for session_id in room_data.session:
                db_session = database.query(Session).filter(Session.id == session_id).first()
                if not db_session:
                    raise HTTPException(status_code=400, detail=f"Session with id {session_id} not found")

            # Update the related entities with the new foreign key
            database.query(Session).filter(Session.id.in_(room_data.session)).update(
                {Session.room_id: db_room.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_room)

    session_ids = database.query(Session.id).filter(Session.room_id == db_room.id).all()
    response_data = {
        "room": db_room,
        "session_ids": [x[0] for x in session_ids]    }
    return response_data


@app.delete("/room/{room_id}/", response_model=None, tags=["Room"])
async def delete_room(room_id: int, database: Session = Depends(get_db)):
    db_room = database.query(Room).filter(Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    database.delete(db_room)
    database.commit()
    return db_room





############################################
#
#   Session functions
#
############################################

@app.get("/session/", response_model=None, tags=["Session"])
def get_all_session(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Session)
        query = query.options(joinedload(Session.scheduleSlot))
        query = query.options(joinedload(Session.event))
        query = query.options(joinedload(Session.room))
        session_list = query.all()

        # Serialize with relationships included
        result = []
        for session_item in session_list:
            item_dict = session_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if session_item.scheduleSlot:
                related_obj = session_item.scheduleSlot
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['scheduleSlot'] = related_dict
            else:
                item_dict['scheduleSlot'] = None
            if session_item.event:
                related_obj = session_item.event
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['event'] = related_dict
            else:
                item_dict['event'] = None
            if session_item.room:
                related_obj = session_item.room
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['room'] = related_dict
            else:
                item_dict['room'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            speaker_list = database.query(Speaker).join(session_speaker, Speaker.id == session_speaker.c.speaker).filter(session_speaker.c.session == session_item.id).all()
            item_dict['speaker'] = []
            for speaker_obj in speaker_list:
                speaker_dict = speaker_obj.__dict__.copy()
                speaker_dict.pop('_sa_instance_state', None)
                item_dict['speaker'].append(speaker_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Session).all()


@app.get("/session/count/", response_model=None, tags=["Session"])
def get_count_session(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Session entities"""
    count = database.query(Session).count()
    return {"count": count}


@app.get("/session/paginated/", response_model=None, tags=["Session"])
def get_paginated_session(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Session entities"""
    total = database.query(Session).count()
    session_list = database.query(Session).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": session_list
        }

    result = []
    for session_item in session_list:
        speaker_ids = database.query(session_speaker.c.speaker).filter(session_speaker.c.session == session_item.id).all()
        item_data = {
            "session": session_item,
            "speaker_ids": [x[0] for x in speaker_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/session/search/", response_model=None, tags=["Session"])
def search_session(
    database: Session = Depends(get_db)
) -> list:
    """Search Session entities by attributes"""
    query = database.query(Session)


    results = query.all()
    return results


@app.get("/session/{session_id}/", response_model=None, tags=["Session"])
async def get_session(session_id: int, database: Session = Depends(get_db)) -> Session:
    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    speaker_ids = database.query(session_speaker.c.speaker).filter(session_speaker.c.session == db_session.id).all()
    response_data = {
        "session": db_session,
        "speaker_ids": [x[0] for x in speaker_ids],
}
    return response_data



@app.post("/session/", response_model=None, tags=["Session"])
async def create_session(session_data: SessionCreate, database: Session = Depends(get_db)) -> Session:

    if session_data.event is not None:
        db_event = database.query(Event).filter(Event.id == session_data.event).first()
        if not db_event:
            raise HTTPException(status_code=400, detail="Event not found")
    else:
        raise HTTPException(status_code=400, detail="Event ID is required")
    if session_data.room is not None:
        db_room = database.query(Room).filter(Room.id == session_data.room).first()
        if not db_room:
            raise HTTPException(status_code=400, detail="Room not found")
    else:
        raise HTTPException(status_code=400, detail="Room ID is required")
    if session_data.speaker:
        for id in session_data.speaker:
            # Entity already validated before creation
            db_speaker = database.query(Speaker).filter(Speaker.id == id).first()
            if not db_speaker:
                raise HTTPException(status_code=404, detail=f"Speaker with ID {id} not found")

    db_session = Session(
        description=session_data.description,        sessionType=session_data.sessionType,        title=session_data.title,        event_id=session_data.event,        room_id=session_data.room        )

    database.add(db_session)
    database.commit()
    database.refresh(db_session)


    if session_data.speaker:
        for id in session_data.speaker:
            # Entity already validated before creation
            db_speaker = database.query(Speaker).filter(Speaker.id == id).first()
            # Create the association
            association = session_speaker.insert().values(session=db_session.id, speaker=db_speaker.id)
            database.execute(association)
            database.commit()


    speaker_ids = database.query(session_speaker.c.speaker).filter(session_speaker.c.session == db_session.id).all()
    response_data = {
        "session": db_session,
        "speaker_ids": [x[0] for x in speaker_ids],
    }
    return response_data


@app.post("/session/bulk/", response_model=None, tags=["Session"])
async def bulk_create_session(items: list[SessionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Session entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.event:
                raise ValueError("Event ID is required")
            if not item_data.room:
                raise ValueError("Room ID is required")

            db_session = Session(
                description=item_data.description,                sessionType=item_data.sessionType,                title=item_data.title,                event_id=item_data.event,                room_id=item_data.room            )
            database.add(db_session)
            database.flush()  # Get ID without committing
            created_items.append(db_session.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Session entities"
    }


@app.delete("/session/bulk/", response_model=None, tags=["Session"])
async def bulk_delete_session(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Session entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_session = database.query(Session).filter(Session.id == item_id).first()
        if db_session:
            database.delete(db_session)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Session entities"
    }

@app.put("/session/{session_id}/", response_model=None, tags=["Session"])
async def update_session(session_id: int, session_data: SessionCreate, database: Session = Depends(get_db)) -> Session:
    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    setattr(db_session, 'description', session_data.description)
    setattr(db_session, 'sessionType', session_data.sessionType)
    setattr(db_session, 'title', session_data.title)
    if session_data.event is not None:
        db_event = database.query(Event).filter(Event.id == session_data.event).first()
        if not db_event:
            raise HTTPException(status_code=400, detail="Event not found")
        setattr(db_session, 'event_id', session_data.event)
    if session_data.room is not None:
        db_room = database.query(Room).filter(Room.id == session_data.room).first()
        if not db_room:
            raise HTTPException(status_code=400, detail="Room not found")
        setattr(db_session, 'room_id', session_data.room)
    existing_speaker_ids = [assoc.speaker for assoc in database.execute(
        session_speaker.select().where(session_speaker.c.session == db_session.id))]

    speakers_to_remove = set(existing_speaker_ids) - set(session_data.speaker)
    for speaker_id in speakers_to_remove:
        association = session_speaker.delete().where(
            (session_speaker.c.session == db_session.id) & (session_speaker.c.speaker == speaker_id))
        database.execute(association)

    new_speaker_ids = set(session_data.speaker) - set(existing_speaker_ids)
    for speaker_id in new_speaker_ids:
        db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
        if db_speaker is None:
            raise HTTPException(status_code=404, detail=f"Speaker with ID {speaker_id} not found")
        association = session_speaker.insert().values(speaker=db_speaker.id, session=db_session.id)
        database.execute(association)
    database.commit()
    database.refresh(db_session)

    speaker_ids = database.query(session_speaker.c.speaker).filter(session_speaker.c.session == db_session.id).all()
    response_data = {
        "session": db_session,
        "speaker_ids": [x[0] for x in speaker_ids],
    }
    return response_data


@app.delete("/session/{session_id}/", response_model=None, tags=["Session"])
async def delete_session(session_id: int, database: Session = Depends(get_db)):
    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    database.delete(db_session)
    database.commit()
    return db_session

@app.post("/session/{session_id}/speaker/{speaker_id}/", response_model=None, tags=["Session Relationships"])
async def add_speaker_to_session(session_id: int, speaker_id: int, database: Session = Depends(get_db)):
    """Add a Speaker to this Session's speaker relationship"""
    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    db_speaker = database.query(Speaker).filter(Speaker.id == speaker_id).first()
    if db_speaker is None:
        raise HTTPException(status_code=404, detail="Speaker not found")

    # Check if relationship already exists
    existing = database.query(session_speaker).filter(
        (session_speaker.c.session == session_id) &
        (session_speaker.c.speaker == speaker_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = session_speaker.insert().values(session=session_id, speaker=speaker_id)
    database.execute(association)
    database.commit()

    return {"message": "Speaker added to speaker successfully"}


@app.delete("/session/{session_id}/speaker/{speaker_id}/", response_model=None, tags=["Session Relationships"])
async def remove_speaker_from_session(session_id: int, speaker_id: int, database: Session = Depends(get_db)):
    """Remove a Speaker from this Session's speaker relationship"""
    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check if relationship exists
    existing = database.query(session_speaker).filter(
        (session_speaker.c.session == session_id) &
        (session_speaker.c.speaker == speaker_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = session_speaker.delete().where(
        (session_speaker.c.session == session_id) &
        (session_speaker.c.speaker == speaker_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Speaker removed from speaker successfully"}


@app.get("/session/{session_id}/speaker/", response_model=None, tags=["Session Relationships"])
async def get_speaker_of_session(session_id: int, database: Session = Depends(get_db)):
    """Get all Speaker entities related to this Session through speaker"""
    db_session = database.query(Session).filter(Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    speaker_ids = database.query(session_speaker.c.speaker).filter(session_speaker.c.session == session_id).all()
    speaker_list = database.query(Speaker).filter(Speaker.id.in_([id[0] for id in speaker_ids])).all()

    return {
        "session_id": session_id,
        "speaker_count": len(speaker_list),
        "speaker": speaker_list
    }





############################################
#
#   Event functions
#
############################################

@app.get("/event/", response_model=None, tags=["Event"])
def get_all_event(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Event)
        event_list = query.all()

        # Serialize with relationships included
        result = []
        for event_item in event_list:
            item_dict = event_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            session_list = database.query(Session).filter(Session.event_id == event_item.id).all()
            item_dict['session'] = []
            for session_obj in session_list:
                session_dict = session_obj.__dict__.copy()
                session_dict.pop('_sa_instance_state', None)
                item_dict['session'].append(session_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Event).all()


@app.get("/event/count/", response_model=None, tags=["Event"])
def get_count_event(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Event entities"""
    count = database.query(Event).count()
    return {"count": count}


@app.get("/event/paginated/", response_model=None, tags=["Event"])
def get_paginated_event(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Event entities"""
    total = database.query(Event).count()
    event_list = database.query(Event).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": event_list
        }

    result = []
    for event_item in event_list:
        session_ids = database.query(Session.id).filter(Session.event_id == event_item.id).all()
        item_data = {
            "event": event_item,
            "session_ids": [x[0] for x in session_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/event/search/", response_model=None, tags=["Event"])
def search_event(
    database: Session = Depends(get_db)
) -> list:
    """Search Event entities by attributes"""
    query = database.query(Event)


    results = query.all()
    return results


@app.get("/event/{event_id}/", response_model=None, tags=["Event"])
async def get_event(event_id: int, database: Session = Depends(get_db)) -> Event:
    db_event = database.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    session_ids = database.query(Session.id).filter(Session.event_id == db_event.id).all()
    response_data = {
        "event": db_event,
        "session_ids": [x[0] for x in session_ids]}
    return response_data



@app.post("/event/", response_model=None, tags=["Event"])
async def create_event(event_data: EventCreate, database: Session = Depends(get_db)) -> Event:


    db_event = Event(
        name=event_data.name,        location=event_data.location,        startDate=event_data.startDate,        endDate=event_data.endDate        )

    database.add(db_event)
    database.commit()
    database.refresh(db_event)

    if event_data.session:
        # Validate that all Session IDs exist
        for session_id in event_data.session:
            db_session = database.query(Session).filter(Session.id == session_id).first()
            if not db_session:
                raise HTTPException(status_code=400, detail=f"Session with id {session_id} not found")

        # Update the related entities with the new foreign key
        database.query(Session).filter(Session.id.in_(event_data.session)).update(
            {Session.event_id: db_event.id}, synchronize_session=False
        )
        database.commit()



    session_ids = database.query(Session.id).filter(Session.event_id == db_event.id).all()
    response_data = {
        "event": db_event,
        "session_ids": [x[0] for x in session_ids]    }
    return response_data


@app.post("/event/bulk/", response_model=None, tags=["Event"])
async def bulk_create_event(items: list[EventCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Event entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_event = Event(
                name=item_data.name,                location=item_data.location,                startDate=item_data.startDate,                endDate=item_data.endDate            )
            database.add(db_event)
            database.flush()  # Get ID without committing
            created_items.append(db_event.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Event entities"
    }


@app.delete("/event/bulk/", response_model=None, tags=["Event"])
async def bulk_delete_event(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Event entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_event = database.query(Event).filter(Event.id == item_id).first()
        if db_event:
            database.delete(db_event)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Event entities"
    }

@app.put("/event/{event_id}/", response_model=None, tags=["Event"])
async def update_event(event_id: int, event_data: EventCreate, database: Session = Depends(get_db)) -> Event:
    db_event = database.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    setattr(db_event, 'name', event_data.name)
    setattr(db_event, 'location', event_data.location)
    setattr(db_event, 'startDate', event_data.startDate)
    setattr(db_event, 'endDate', event_data.endDate)
    if event_data.session is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Session).filter(Session.event_id == db_event.id).update(
            {Session.event_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if event_data.session:
            # Validate that all IDs exist
            for session_id in event_data.session:
                db_session = database.query(Session).filter(Session.id == session_id).first()
                if not db_session:
                    raise HTTPException(status_code=400, detail=f"Session with id {session_id} not found")

            # Update the related entities with the new foreign key
            database.query(Session).filter(Session.id.in_(event_data.session)).update(
                {Session.event_id: db_event.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_event)

    session_ids = database.query(Session.id).filter(Session.event_id == db_event.id).all()
    response_data = {
        "event": db_event,
        "session_ids": [x[0] for x in session_ids]    }
    return response_data


@app.delete("/event/{event_id}/", response_model=None, tags=["Event"])
async def delete_event(event_id: int, database: Session = Depends(get_db)):
    db_event = database.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    database.delete(db_event)
    database.commit()
    return db_event







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



