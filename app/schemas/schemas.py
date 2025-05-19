from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Metric type schemas
class MetricTypeBase(BaseModel):
    name: str
    unit: str
    description: str = ""

class MetricTypeCreate(MetricTypeBase):
    pass

class MetricType(MetricTypeBase):
    id: int
    
    class Config:
        orm_mode = True

# Health metric schemas
class HealthMetricBase(BaseModel):
    metric_type_id: int
    value: float
    notes: Optional[str] = None

class HealthMetricCreate(HealthMetricBase):
    pass

class HealthMetric(HealthMetricBase):
    id: int
    user_id: int
    recorded_at: datetime
    metric_type: MetricType
    
    class Config:
        orm_mode = True

# Exercise type schemas
class ExerciseTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExerciseTypeCreate(ExerciseTypeBase):
    pass

class ExerciseType(ExerciseTypeBase):
    id: int
    
    class Config:
        orm_mode = True

# Exercise record schemas
class ExerciseRecordBase(BaseModel):
    exercise_type_id: int
    duration: int  # in seconds
    distance: Optional[float] = None  # in meters
    calories: Optional[float] = None
    heart_rate_avg: Optional[float] = None
    notes: Optional[str] = None

class ExerciseRecordCreate(ExerciseRecordBase):
    pass

class ExerciseRecord(ExerciseRecordBase):
    id: int
    user_id: int
    recorded_at: datetime
    exercise_type: ExerciseType
    
    class Config:
        orm_mode = True

# Simple data schema for quick logging via URL
class SimpleDataLog(BaseModel):
    type: str  # Metric or exercise type name
    value: float  # Metric value or exercise duration
    extra: Optional[dict] = None  # Extra data (distance, calories, etc.)
