import pytest
import sys
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add project root to path to make imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Updated import path for the app
from src.api.app import app as application

@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {}
    return application

@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)
