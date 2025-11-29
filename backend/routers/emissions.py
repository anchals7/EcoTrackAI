"""
Emissions tracking and forecasting endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from models.schemas import DailyEmissionsResponse, WeeklyEmissionsResponse, ForecastResponse
from services.prophet_service import generate_forecast
from collections import defaultdict
from services.database import execute_query, connection_pool
from routers.activities import activities_db_fallback

router = APIRouter()

def get_activities():
    """Get activities from database or fallback"""
    if connection_pool:
        try:
            query = "SELECT * FROM activities ORDER BY date DESC"
            return execute_query(query)
        except Exception as e:
            print(f"Database error: {e}, using fallback")
            return activities_db_fallback
    else:
        return activities_db_fallback

@router.get("/daily")
async def get_daily_emissions(date: str = None):
    """
    Get daily emissions summary
    
    If date is not provided, returns today's emissions
    """
    if date:
        target_date = datetime.fromisoformat(date).date()
    else:
        target_date = datetime.now().date()
    
    # Get activities
    all_activities = get_activities()
    
    # Filter activities for the target date
    daily_activities = []
    for act in all_activities:
        act_date = act.get("date")
        if act_date:
            if isinstance(act_date, str):
                act_date = datetime.fromisoformat(act_date.replace('Z', '+00:00'))
            if isinstance(act_date, datetime):
                if act_date.date() == target_date:
                    daily_activities.append(act)
    
    total_co2e = sum(float(act.get("co2e_kg", 0)) for act in daily_activities)
    
    return {
        "date": str(target_date),
        "total_co2e_kg": total_co2e,
        "activities": daily_activities,
        "activity_count": len(daily_activities)
    }

@router.get("/weekly")
async def get_weekly_emissions(week_start: str = None):
    """
    Get weekly emissions summary
    
    If week_start is not provided, uses current week
    """
    if week_start:
        start_date = datetime.fromisoformat(week_start).date()
    else:
        # Get start of current week (Monday)
        today = datetime.now().date()
        days_since_monday = today.weekday()
        start_date = today - timedelta(days=days_since_monday)
    
    end_date = start_date + timedelta(days=6)
    
    # Get activities
    all_activities = get_activities()
    
    # Filter activities for the week
    weekly_activities = []
    for act in all_activities:
        act_date = act.get("date")
        if act_date:
            if isinstance(act_date, str):
                act_date = datetime.fromisoformat(act_date.replace('Z', '+00:00'))
            if isinstance(act_date, datetime):
                if start_date <= act_date.date() <= end_date:
                    weekly_activities.append(act)
    
    total_co2e = sum(float(act.get("co2e_kg", 0)) for act in weekly_activities)
    
    # Group by date for daily breakdown
    daily_breakdown = defaultdict(lambda: {"date": "", "total_co2e_kg": 0.0, "activities": []})
    
    for act in weekly_activities:
        act_date = act.get("date")
        if act_date:
            if isinstance(act_date, str):
                act_date = datetime.fromisoformat(act_date.replace('Z', '+00:00'))
            if isinstance(act_date, datetime):
                date_str = str(act_date.date())
                daily_breakdown[date_str]["date"] = date_str
                # Ensure co2e_kg is a float
                co2e_value = float(act.get("co2e_kg", 0))
                daily_breakdown[date_str]["total_co2e_kg"] += co2e_value
                daily_breakdown[date_str]["activities"].append(act)
    
    # Category breakdown
    category_breakdown = defaultdict(float)
    for act in weekly_activities:
        category = act.get("activity_category", "unknown")
        co2e_value = float(act.get("co2e_kg", 0))
        category_breakdown[category] += co2e_value
    
    return {
        "week_start": str(start_date),
        "week_end": str(end_date),
        "total_co2e_kg": total_co2e,
        "daily_breakdown": list(daily_breakdown.values()),
        "category_breakdown": dict(category_breakdown),
        "activity_count": len(weekly_activities)
    }

@router.get("/predict")
async def get_emissions_forecast(days_ahead: int = 7):
    """
    Get emissions forecast using Prophet
    
    Requires at least 7 days of historical data
    """
    all_activities = get_activities()
    
    if len(all_activities) < 7:
        raise HTTPException(
            status_code=400,
            detail="Need at least 7 days of activity data for forecasting"
        )
    
    # Group activities by date
    daily_emissions = defaultdict(float)
    for act in all_activities:
        act_date = act.get("date")
        if act_date:
            if isinstance(act_date, str):
                act_date = datetime.fromisoformat(act_date.replace('Z', '+00:00'))
            if isinstance(act_date, datetime):
                date_str = str(act_date.date())
                daily_emissions[date_str] += float(act.get("co2e_kg", 0))
    
    # Prepare historical data
    historical_data = [
        {"date": date, "total_emissions": emissions}
        for date, emissions in sorted(daily_emissions.items())
    ]
    
    # Generate forecast
    forecast = generate_forecast(historical_data, days_ahead)
    
    return forecast

@router.get("/summary")
async def get_emissions_summary():
    """Get overall emissions summary"""
    all_activities = get_activities()
    
    if not all_activities:
        return {
            "total_emissions_kg": 0.0,
            "total_activities": 0,
            "category_breakdown": {},
            "date_range": None
        }
    
    total_emissions = sum(float(act.get("co2e_kg", 0)) for act in all_activities)
    
    category_breakdown = defaultdict(float)
    for act in all_activities:
        category_breakdown[act.get("activity_category", "unknown")] += float(act.get("co2e_kg", 0))
    
    dates = []
    for act in all_activities:
        act_date = act.get("date")
        if act_date:
            if isinstance(act_date, str):
                act_date = datetime.fromisoformat(act_date.replace('Z', '+00:00'))
            if isinstance(act_date, datetime):
                dates.append(act_date)
    
    date_range = None
    if dates:
        date_range = {
            "earliest": min(dates).isoformat(),
            "latest": max(dates).isoformat()
        }
    
    return {
        "total_emissions_kg": total_emissions,
        "total_activities": len(all_activities),
        "category_breakdown": dict(category_breakdown),
        "date_range": date_range
    }

