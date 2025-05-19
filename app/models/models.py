from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    health_metrics = relationship("HealthMetric", back_populates="user")
    exercise_records = relationship("ExerciseRecord", back_populates="user")

class MetricType(Base):
    __tablename__ = "metric_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    unit = Column(String)
    description = Column(String)
    
    # Relationships
    health_metrics = relationship("HealthMetric", back_populates="metric_type")

class HealthMetric(Base):
    __tablename__ = "health_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    metric_type_id = Column(Integer, ForeignKey("metric_types.id"))
    value = Column(Float)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="health_metrics")
    metric_type = relationship("MetricType", back_populates="health_metrics")

class ExerciseType(Base):
    __tablename__ = "exercise_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Relationships
    exercise_records = relationship("ExerciseRecord", back_populates="exercise_type")

class ExerciseRecord(Base):
    __tablename__ = "exercise_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exercise_type_id = Column(Integer, ForeignKey("exercise_types.id"))
    duration = Column(Integer)  # Duration in seconds
    distance = Column(Float, nullable=True)  # Distance in meters
    calories = Column(Float, nullable=True)  # Calories burned
    heart_rate_avg = Column(Float, nullable=True)  # Average heart rate
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="exercise_records")
    exercise_type = relationship("ExerciseType", back_populates="exercise_records")
