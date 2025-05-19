from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.models import HealthMetric, MetricType, User
from app.schemas.schemas import HealthMetricCreate, HealthMetric as HealthMetricSchema

router = APIRouter()

@router.post("/", response_model=HealthMetricSchema)
def create_health_metric(
    metric: HealthMetricCreate, 
    user_id: int, 
    db: Session = Depends(get_db)
):
    """Create a new health metric record"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify metric type exists
    metric_type = db.query(MetricType).filter(MetricType.id == metric.metric_type_id).first()
    if not metric_type:
        raise HTTPException(status_code=404, detail="Metric type not found")
    
    # Create health metric
    db_metric = HealthMetric(
        user_id=user_id,
        metric_type_id=metric.metric_type_id,
        value=metric.value,
        notes=metric.notes,
        recorded_at=datetime.utcnow()
    )
    
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/", response_model=List[HealthMetricSchema])
def read_health_metrics(
    user_id: int,
    metric_type_id: int = None,
    skip: int = 0,
    limit: int = 100,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    """Get health metrics with filters"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(HealthMetric).filter(HealthMetric.user_id == user_id)
    
    # Apply filters
    if metric_type_id:
        query = query.filter(HealthMetric.metric_type_id == metric_type_id)
    
    if start_date:
        query = query.filter(HealthMetric.recorded_at >= start_date)
        
    if end_date:
        query = query.filter(HealthMetric.recorded_at <= end_date)
    
    # Apply pagination
    metrics = query.order_by(HealthMetric.recorded_at.desc()).offset(skip).limit(limit).all()
    
    return metrics

@router.get("/{metric_id}", response_model=HealthMetricSchema)
def read_health_metric(
    metric_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific health metric by ID"""
    metric = db.query(HealthMetric).filter(
        HealthMetric.id == metric_id,
        HealthMetric.user_id == user_id
    ).first()
    
    if not metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    
    return metric

@router.delete("/{metric_id}")
def delete_health_metric(
    metric_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a health metric"""
    metric = db.query(HealthMetric).filter(
        HealthMetric.id == metric_id,
        HealthMetric.user_id == user_id
    ).first()
    
    if not metric:
        raise HTTPException(status_code=404, detail="Health metric not found")
    
    db.delete(metric)
    db.commit()
    
    return {"message": "Health metric deleted successfully"}
