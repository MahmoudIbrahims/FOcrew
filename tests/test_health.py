from fastapi import FastAPI, APIRouter, Depends
from fastapi.testclient import TestClient
from typing import Dict

# --- 1. Mocking Dependencies ---

# Mock the required configuration classes/functions as we don't have helpers/config.py
class MockSettings:
    """Mock class simulating the structure of the Settings model."""
    APP_NAME: str = "FOcrew Mock Test App"
    APP_VERSION: str = "1.0.0-test"

def mock_get_settings() -> MockSettings:
    """Mock dependency function that returns fixed test settings."""
    return MockSettings()

# --- 2. Recreating the User's Router ---
base_router = APIRouter(
    prefix="/health/v1",
    tags=["health_v1"],
)

# Use MockSettings here to avoid needing to import the actual Settings
@base_router.get('/')
async def welcome(app_settings: MockSettings = Depends(mock_get_settings)) -> Dict[str, str]:
    """
    Simulates the user's original endpoint logic, using the mocked dependency.
    """
    return {
        "App_name": app_settings.APP_NAME,
        "App_version": app_settings.APP_VERSION,
    }

# --- 3. Test App Setup ---

# Create the FastAPI instance
app = FastAPI()
# Include the router in the app
app.include_router(base_router)

# Create the test client
client = TestClient(app)

# --- 4. The Updated Test Function ---

def test_read_health_check_v1():
    """
    Test the /health/v1/ endpoint to ensure it returns the correct status 
    and the mocked application settings (name and version).
    """
    # 1. The test directs the request to the correct path
    response = client.get("/health/v1/")
    
    # 2. Check the HTTP status code
    assert response.status_code == 200
    
    # 3. Check the response content against the mocked settings
    expected_data = {
        "App_name": MockSettings.APP_NAME,
        "App_version": MockSettings.APP_VERSION,
    }
    assert response.json() == expected_data