import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.models import User, MetricType, HealthMetric, ExerciseType
from app.schemas.schemas import UserCreate, MetricTypeCreate, ExerciseTypeCreate

def test_user_model():
    """测试用户模型"""
    user = User(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_metric_type_model():
    """测试指标类型模型"""
    metric_type = MetricType(name="weight", unit="kg", description="Body weight")
    assert metric_type.name == "weight"
    assert metric_type.unit == "kg"
    assert metric_type.description == "Body weight"

def test_exercise_type_model():
    """测试运动类型模型"""
    exercise_type = ExerciseType(name="running", description="Running or jogging")
    assert exercise_type.name == "running"
    assert exercise_type.description == "Running or jogging"

def test_user_schema():
    """测试用户模式验证"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    user_schema = UserCreate(**user_data)
    assert user_schema.username == "testuser"
    assert user_schema.email == "test@example.com"

def test_metric_type_schema():
    """测试指标类型模式验证"""
    metric_data = {
        "name": "weight",
        "unit": "kg",
        "description": "Body weight"
    }
    metric_schema = MetricTypeCreate(**metric_data)
    assert metric_schema.name == "weight"
    assert metric_schema.unit == "kg"
    assert metric_schema.description == "Body weight"

def test_exercise_type_schema():
    """测试运动类型模式验证"""
    exercise_data = {
        "name": "running",
        "description": "Running or jogging"
    }
    exercise_schema = ExerciseTypeCreate(**exercise_data)
    assert exercise_schema.name == "running"
    assert exercise_schema.description == "Running or jogging"
