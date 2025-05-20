import pytest
import os
import sys
import json
from fastapi.testclient import TestClient

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)

def test_root_endpoint():
    """测试根端点"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to" in response.json()["message"]
    assert "documentation" in response.json()

def test_api_docs():
    """测试API文档端点"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()

def test_openapi_schema():
    """测试OpenAPI模式"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "components" in schema
    assert "schemas" in schema["components"]

# 以下测试需要在测试前初始化数据库，
# 在实际CI环境中运行时可能需要模拟数据库或使用测试数据库
