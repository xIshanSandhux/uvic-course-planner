from typing import List, Dict, Any, Optional, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    timestamp: datetime = datetime.now()
    

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    timestamp: datetime = datetime.now()

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: Optional[str] = None
    timestamp: datetime = datetime.now()