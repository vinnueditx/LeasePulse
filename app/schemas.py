from enum import Enum
from pydantic import BaseModel, Field

class FurnishedStatus(str, Enum):
    NO = "No"
    SEMI = "Semi"
    YES = "Yes"

class ParkingStatus(str, Enum):
    NO = "No"
    YES = "Yes"

class HouseRequest(BaseModel):
    area: float = Field(..., gt=100, description="House area in square feet")
    bedrooms: int = Field(..., ge=1, le=10)
    bathrooms: int = Field(..., ge=1, le=10)
    age: int = Field(..., ge=0, le=100)
    location: str
    furnished: FurnishedStatus
    parking: ParkingStatus
