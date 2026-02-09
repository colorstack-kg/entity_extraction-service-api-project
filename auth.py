from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

header_scheme = APIKeyHeader(name="X-API-Key", auto_error=True)

def check_api_key(key):
    return key == API_KEY

def validate_auth(api_key: str = Security(header_scheme)):
    if check_api_key(api_key):
        return "api_key"

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )