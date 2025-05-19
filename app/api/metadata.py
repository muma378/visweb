from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import User, MetricType, ExerciseType
from app.schemas.schemas import (
    UserCreate, User as UserSchema,
    MetricTypeCreate, MetricType as MetricTypeSchema,
    ExerciseTypeCreate, ExerciseType as ExerciseTypeSchema
)

router = APIRouter()

# User routes
@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Metric types routes
@router.post("/metric-types/", response_model=MetricTypeSchema)
def create_metric_type(metric_type: MetricTypeCreate, db: Session = Depends(get_db)):
    """Create a new metric type"""
    # Check if metric type already exists
    db_metric_type = db.query(MetricType).filter(MetricType.name == metric_type.name).first()
    if db_metric_type:
        raise HTTPException(status_code=400, detail="Metric type already exists")
    
    # Create metric type
    db_metric_type = MetricType(**metric_type.dict())
    db.add(db_metric_type)
    db.commit()
    db.refresh(db_metric_type)
    
    return db_metric_type

@router.get("/metric-types/", response_model=List[MetricTypeSchema])
def read_metric_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all metric types"""
    metric_types = db.query(MetricType).offset(skip).limit(limit).all()
    return metric_types

@router.get("/metric-types/{metric_type_id}", response_model=MetricTypeSchema)
def read_metric_type(metric_type_id: int, db: Session = Depends(get_db)):
    """Get a specific metric type by ID"""
    metric_type = db.query(MetricType).filter(MetricType.id == metric_type_id).first()
    if not metric_type:
        raise HTTPException(status_code=404, detail="Metric type not found")
    return metric_type

# Exercise types routes
@router.post("/exercise-types/", response_model=ExerciseTypeSchema)
def create_exercise_type(exercise_type: ExerciseTypeCreate, db: Session = Depends(get_db)):
    """Create a new exercise type"""
    # Check if exercise type already exists
    db_exercise_type = db.query(ExerciseType).filter(ExerciseType.name == exercise_type.name).first()
    if db_exercise_type:
        raise HTTPException(status_code=400, detail="Exercise type already exists")
    
    # Create exercise type
    db_exercise_type = ExerciseType(**exercise_type.dict())
    db.add(db_exercise_type)
    db.commit()
    db.refresh(db_exercise_type)
    
    return db_exercise_type

@router.get("/exercise-types/", response_model=List[ExerciseTypeSchema])
def read_exercise_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all exercise types"""
    exercise_types = db.query(ExerciseType).offset(skip).limit(limit).all()
    return exercise_types

@router.get("/exercise-types/{exercise_type_id}", response_model=ExerciseTypeSchema)
def read_exercise_type(exercise_type_id: int, db: Session = Depends(get_db)):
    """Get a specific exercise type by ID"""
    exercise_type = db.query(ExerciseType).filter(ExerciseType.id == exercise_type_id).first()
    if not exercise_type:
        raise HTTPException(status_code=404, detail="Exercise type not found")
    return exercise_type
