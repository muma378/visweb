import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import Base, get_db
from app.models.models import User, MetricType, HealthMetric, ExerciseType, ExerciseRecord
from app import app

# 创建测试数据库引擎
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# 创建测试会话
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def setup_test_db():
    """设置测试数据库"""
    # 创建表
    Base.metadata.create_all(bind=engine)
    
    # 提供测试会话
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    # 替换依赖项
    app.dependency_overrides[get_db] = override_get_db
    
    # 提供数据库会话供测试使用
    db = TestingSessionLocal()
    
    # 初始化一些测试数据
    test_user = User(username="testuser", email="test@example.com")
    db.add(test_user)
    db.commit()
    
    weight_type = MetricType(name="weight", unit="kg", description="Body weight")
    steps_type = MetricType(name="steps", unit="count", description="Steps taken")
    db.add(weight_type)
    db.add(steps_type)
    db.commit()
    
    running_type = ExerciseType(name="running", description="Running or jogging")
    db.add(running_type)
    db.commit()
    
    yield db
    
    # 测试后清理
    db.close()
    Base.metadata.drop_all(bind=engine)
    
    if os.path.exists("./test.db"):
        os.remove("./test.db")
        
    # 移除依赖项覆盖
    app.dependency_overrides = {}
