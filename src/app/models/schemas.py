from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime

# Health Schemas
class HealthResponse(BaseModel):
    status: str
    timestamp: float
    service: str

# Data Schemas
class DataResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    metadata: Optional[dict] = None

class Metadata(BaseModel):
    processed_at: float
    source: str

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserOperationResponse(BaseModel):
    success: bool
    user: UserResponse
    message: str

# Slow Operation Schemas
class SlowOperationResponse(BaseModel):
    success: bool
    message: str
    processing_time: float

# Error Schemas
class ErrorResponse(BaseModel):
    success: bool
    error: str
