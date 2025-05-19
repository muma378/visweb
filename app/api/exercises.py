from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.models import ExerciseRecord, ExerciseType, User
from app.schemas.schemas import ExerciseRecordCreate, ExerciseRecord as ExerciseRecordSchema

router = APIRouter()

@router.post("/", response_model=ExerciseRecordSchema)
def create_exercise_record(
    exercise: ExerciseRecordCreate, 
    user_id: int, 
    db: Session = Depends(get_db)
):
    """Create a new exercise record"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify exercise type exists
    exercise_type = db.query(ExerciseType).filter(ExerciseType.id == exercise.exercise_type_id).first()
    if not exercise_type:
        raise HTTPException(status_code=404, detail="Exercise type not found")
    
    # Create exercise record
    db_exercise = ExerciseRecord(
        user_id=user_id,
        exercise_type_id=exercise.exercise_type_id,
        duration=exercise.duration,
        distance=exercise.distance,
        calories=exercise.calories,
        heart_rate_avg=exercise.heart_rate_avg,
        notes=exercise.notes,
        recorded_at=datetime.utcnow()
    )
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/", response_model=List[ExerciseRecordSchema])
def read_exercise_records(
    user_id: int,
    exercise_type_id: int = None,
    skip: int = 0,
    limit: int = 100,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    """Get exercise records with filters"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(ExerciseRecord).filter(ExerciseRecord.user_id == user_id)
    
    # Apply filters
    if exercise_type_id:
        query = query.filter(ExerciseRecord.exercise_type_id == exercise_type_id)
    
    if start_date:
        query = query.filter(ExerciseRecord.recorded_at >= start_date)
        
    if end_date:
        query = query.filter(ExerciseRecord.recorded_at <= end_date)
    
    # Apply pagination
    exercises = query.order_by(ExerciseRecord.recorded_at.desc()).offset(skip).limit(limit).all()
    
    return exercises

@router.get("/{exercise_id}", response_model=ExerciseRecordSchema)
def read_exercise_record(
    exercise_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific exercise record by ID"""
    exercise = db.query(ExerciseRecord).filter(
        ExerciseRecord.id == exercise_id,
        ExerciseRecord.user_id == user_id
    ).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise record not found")
    
    return exercise

@router.delete("/{exercise_id}")
def delete_exercise_record(
    exercise_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete an exercise record"""
    exercise = db.query(ExerciseRecord).filter(
        ExerciseRecord.id == exercise_id,
        ExerciseRecord.user_id == user_id
    ).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise record not found")
    
    db.delete(exercise)
    db.commit()
    
    return {"message": "Exercise record deleted successfully"}
