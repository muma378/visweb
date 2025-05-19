from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.db.database import get_db
from app.models.models import User, MetricType, HealthMetric, ExerciseType, ExerciseRecord
from app.schemas.schemas import SimpleDataLog

router = APIRouter()

@router.get("/log")
def log_data_via_url(
    user_id: int,
    type: str,
    value: float,
    distance: Optional[float] = None,
    calories: Optional[float] = None,
    heart_rate: Optional[float] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Log data via URL parameters for easy data collection.
    Example:
        /api/quick/log?user_id=1&type=weight&value=80.5
        /api/quick/log?user_id=1&type=running&value=30&distance=5000&calories=300
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Try to find metric type first
    metric_type = db.query(MetricType).filter(MetricType.name == type).first()
    if metric_type:
        # This is a health metric
        db_metric = HealthMetric(
            user_id=user_id,
            metric_type_id=metric_type.id,
            value=value,
            notes=notes,
            recorded_at=datetime.utcnow()
        )
        
        db.add(db_metric)
        db.commit()
        db.refresh(db_metric)
        
        return {
            "status": "success",
            "message": f"Health metric '{type}' logged successfully",
            "data": {
                "id": db_metric.id,
                "type": metric_type.name,
                "value": db_metric.value,
                "unit": metric_type.unit,
                "recorded_at": db_metric.recorded_at
            }
        }
    
    # If not a health metric, try exercise type
    exercise_type = db.query(ExerciseType).filter(ExerciseType.name == type).first()
    if exercise_type:
        # This is an exercise record
        db_exercise = ExerciseRecord(
            user_id=user_id,
            exercise_type_id=exercise_type.id,
            duration=int(value),  # Value is duration in seconds for exercises
            distance=distance,
            calories=calories,
            heart_rate_avg=heart_rate,
            notes=notes,
            recorded_at=datetime.utcnow()
        )
        
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        
        return {
            "status": "success",
            "message": f"Exercise '{type}' logged successfully",
            "data": {
                "id": db_exercise.id,
                "type": exercise_type.name,
                "duration": db_exercise.duration,
                "distance": db_exercise.distance,
                "calories": db_exercise.calories,
                "recorded_at": db_exercise.recorded_at
            }
        }
    
    # If type not found
    raise HTTPException(
        status_code=404,
        detail=f"Type '{type}' not found. Please create this metric or exercise type first."
    )
