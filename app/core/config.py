import os
from pydantic import BaseModel

is_serverless = (
    os.getenv("VERCEL") == "1" 
    or "AWS_LAMBDA_FUNCTION_NAME" in os.environ 
    or os.getenv("VERCEL_ENV") is not None
)
_default_data_dir = "/tmp/data" if is_serverless else "./data"
_default_reports_dir = "/tmp/data/reports" if is_serverless else "./data/reports"
_default_db_url = "sqlite:////tmp/data/estate_ops.db" if is_serverless else "sqlite:///./data/estate_ops.db"

class Settings(BaseModel):
    APP_NAME: str = "Real Estate AI Operations Platform"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-jwt-key-replace-in-production-estate-ai-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    DATABASE_URL: str = os.getenv("DATABASE_URL", _default_db_url)
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock_and_openmaus")
    DEFAULT_CURRENCY: str = "INR"
    SECONDARY_CURRENCY: str = "USD"
    INITIAL_TARGET_CITY: str = "Hyderabad"
    INITIAL_TARGET_STATE: str = "Telangana"
    INITIAL_TARGET_COUNTRY: str = "India"
    DATA_DIR: str = os.getenv("DATA_DIR", _default_data_dir)
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", _default_reports_dir)

settings = Settings()
