"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Activity Logging Models
class ActivityLogRequest(BaseModel):
    """Request model for logging an activity"""
    text: Optional[str] = Field(None, description="Natural language description of activity")
    category: Optional[str] = Field(None, description="Activity category (transportation, food, energy, etc.)")
    subtype: Optional[str] = Field(None, description="Activity subtype (car, beef, electricity, etc.)")
    amount: Optional[float] = Field(None, description="Amount of activity")
    unit: Optional[str] = Field(None, description="Unit of measurement (miles, kg, kWh, etc.)")
    date: Optional[datetime] = Field(None, description="Date of activity (defaults to today)")

class ActivityStructured(BaseModel):
    """Structured activity data from Gemini parsing"""
    category: str
    subtype: str
    amount: float
    unit: str
    description: str

class EmissionRecord(BaseModel):
    """Emission record response"""
    id: str
    user_id: str
    activity_category: str
    activity_subtype: str
    amount: float
    unit: str
    co2e_kg: float
    date: datetime
    created_at: datetime

# Emissions Models
class DailyEmissionsResponse(BaseModel):
    """Daily emissions summary"""
    date: str
    total_co2e_kg: float
    activities: List[EmissionRecord]

class WeeklyEmissionsResponse(BaseModel):
    """Weekly emissions summary"""
    week_start: str
    week_end: str
    total_co2e_kg: float
    daily_breakdown: List[DailyEmissionsResponse]
    category_breakdown: Dict[str, float]

# Forecasting Models
class ForecastResponse(BaseModel):
    """Prophet forecast response"""
    predictions: List[Dict[str, Any]]
    next_7_days_total: float
    trend: str  # "increasing", "decreasing", "stable"

# Recommendations Models
class Recommendation(BaseModel):
    """Individual recommendation"""
    title: str
    description: str
    estimated_savings_kg: float
    category: str
    priority: str  # "high", "medium", "low"

class RecommendationsResponse(BaseModel):
    """Recommendations response"""
    user_archetype: str
    recommendations: List[Recommendation]
    total_potential_savings_kg: float

# User Models
class UserCreate(BaseModel):
    """User registration"""
    email: str
    password: str
    name: Optional[str] = None

class UserResponse(BaseModel):
    """User response"""
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime

