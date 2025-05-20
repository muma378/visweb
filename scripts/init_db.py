#!/usr/bin/env python3
"""
Initialize the database with sample data.
Run this script after setting up the application to create a test user and common metrics.
"""

import sys
import os
from datetime import datetime, timedelta
import random
import time

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, engine, Base
from app.models.models import User, MetricType, HealthMetric, ExerciseType, ExerciseRecord

# Wait for database to be ready (useful in Docker environment)
def wait_for_db(max_retries=10, retry_interval=2):
    for i in range(max_retries):
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            return True
        except Exception as e:
            print(f"Database not ready yet (attempt {i+1}/{max_retries}): {e}")
            time.sleep(retry_interval)
    
    raise Exception("Could not connect to database after multiple attempts")

def init_db():
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    # Wait for database to be accessible
    wait_for_db()
    
    db = SessionLocal()
    
    try:
        # Create a test user
        test_user = User(
            username="testuser",
            email="test@example.com"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"Created test user: {test_user.username} (ID: {test_user.id})")
        
        # Create common health metric types
        health_metrics = [
            MetricType(name="weight", unit="kg", description="Body weight"),
            MetricType(name="blood_pressure_systolic", unit="mmHg", description="Systolic blood pressure"),
            MetricType(name="blood_pressure_diastolic", unit="mmHg", description="Diastolic blood pressure"),
            MetricType(name="heart_rate", unit="bpm", description="Resting heart rate"),
            MetricType(name="sleep", unit="hours", description="Sleep duration"),
            MetricType(name="steps", unit="count", description="Steps taken"),
            MetricType(name="water", unit="ml", description="Water intake"),
            MetricType(name="temperature", unit="°C", description="Body temperature"),
        ]
        
        for metric in health_metrics:
            db.add(metric)
        
        db.commit()
        
        # Create common exercise types
        exercise_types = [
            ExerciseType(name="running", description="Running or jogging"),
            ExerciseType(name="walking", description="Walking"),
            ExerciseType(name="cycling", description="Cycling or biking"),
            ExerciseType(name="swimming", description="Swimming"),
            ExerciseType(name="weightlifting", description="Weight training"),
            ExerciseType(name="yoga", description="Yoga"),
            ExerciseType(name="hiit", description="High-intensity interval training"),
            ExerciseType(name="basketball", description="Basketball"),
        ]
        
        for exercise in exercise_types:
            db.add(exercise)
        
        db.commit()
        
        print(f"Created {len(health_metrics)} health metric types and {len(exercise_types)} exercise types")
        
        # Generate sample data for the past week
        create_sample_data(db, test_user.id)
        
    finally:
        db.close()

def create_sample_data(db, user_id):
    # Get IDs for sample data generation
    weight_id = db.query(MetricType).filter_by(name="weight").first().id
    steps_id = db.query(MetricType).filter_by(name="steps").first().id
    sleep_id = db.query(MetricType).filter_by(name="sleep").first().id
    
    running_id = db.query(ExerciseType).filter_by(name="running").first().id
    cycling_id = db.query(ExerciseType).filter_by(name="cycling").first().id
    
    # Generate 7 days of data
    today = datetime.now()
    
    for i in range(7):
        day = today - timedelta(days=i)
        day = day.replace(hour=8, minute=0, second=0, microsecond=0)
        
        # Weight (small random variations)
        weight = 75 + random.uniform(-1.0, 1.0)
        db.add(HealthMetric(
            user_id=user_id,
            metric_type_id=weight_id,
            value=round(weight, 1),
            recorded_at=day
        ))
        
        # Steps (random between 5000-12000)
        steps = random.randint(5000, 12000)
        db.add(HealthMetric(
            user_id=user_id,
            metric_type_id=steps_id,
            value=steps,
            recorded_at=day.replace(hour=21)  # End of day
        ))
        
        # Sleep (random between 6-9 hours)
        sleep = random.uniform(6, 9)
        db.add(HealthMetric(
            user_id=user_id,
            metric_type_id=sleep_id,
            value=round(sleep, 1),
            recorded_at=day
        ))
        
        # Add exercise every other day, alternating between running and cycling
        if i % 2 == 0:
            exercise_type_id = running_id
            duration = random.randint(20, 40) * 60  # 20-40 minutes in seconds
            distance = round(duration/60 * random.uniform(150, 180))  # ~2.5-3.0 km per 20 mins
            
            db.add(ExerciseRecord(
                user_id=user_id,
                exercise_type_id=exercise_type_id,
                duration=duration,
                distance=distance,
                calories=round(duration/60 * 10),  # ~10 calories per minute
                heart_rate_avg=random.randint(140, 160),
                recorded_at=day.replace(hour=18)  # Evening workout
            ))
        elif i % 2 == 1:
            exercise_type_id = cycling_id
            duration = random.randint(30, 60) * 60  # 30-60 minutes in seconds
            distance = round(duration/60 * random.uniform(300, 350))  # ~5-6 km per 10 mins
            
            db.add(ExerciseRecord(
                user_id=user_id,
                exercise_type_id=exercise_type_id,
                duration=duration,
                distance=distance,
                calories=round(duration/60 * 8),  # ~8 calories per minute
                heart_rate_avg=random.randint(130, 150),
                recorded_at=day.replace(hour=17, minute=30)  # Evening workout
            ))
    
    db.commit()
    print(f"Generated 7 days of sample data for user ID {user_id}")

if __name__ == "__main__":
    print("Initializing database with sample data...")
    init_db()
    print("Database initialization completed!")
