"""
Activity logging endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from models.schemas import ActivityLogRequest, ActivityStructured, EmissionRecord
from services.gemini_service import parse_activity_text
from services.climatiq_service import calculate_emissions
from services.database import (
    get_db_connection, return_db_connection,
    execute_query, execute_insert_returning,
    connection_pool
)

router = APIRouter()

# Fallback in-memory storage (only used if Supabase is not configured)
activities_db_fallback: List[Dict[str, Any]] = []

def has_database():
    """Check if database is available"""
    return connection_pool is not None

@router.post("/log")
async def log_activity(activity: ActivityLogRequest):
    """
    Log an activity and calculate emissions
    
    Supports both natural language and structured input
    """
    try:
        # Parse natural language if provided
        if activity.text:
            structured = parse_activity_text(activity.text)
            if not structured:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to parse activity from text"
                )
            category = structured.category
            subtype = structured.subtype
            amount = structured.amount
            unit = structured.unit
        else:
            # Use structured input
            if not all([activity.category, activity.subtype, activity.amount, activity.unit]):
                raise HTTPException(
                    status_code=400,
                    detail="Missing required fields: category, subtype, amount, unit"
                )
            category = activity.category
            subtype = activity.subtype
            amount = activity.amount
            unit = activity.unit
        
        # Calculate emissions
        emission_result = calculate_emissions(category, subtype, amount, unit)
        
        if not emission_result:
            raise HTTPException(
                status_code=500,
                detail="Failed to calculate emissions"
            )
        
        # Create emission record
        record_data = {
            "user_id": "user_001",  # TODO: Get from auth
            "activity_category": category,
            "activity_subtype": subtype,
            "amount": float(amount),
            "unit": unit,
            "co2e_kg": float(emission_result["co2e_kg"]),
            "date": activity.date or datetime.now(),
        }
        
        # Save to database or fallback
        if has_database():
            try:
                query = """
                    INSERT INTO activities 
                    (user_id, activity_category, activity_subtype, amount, unit, co2e_kg, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """
                params = (
                    record_data["user_id"],
                    record_data["activity_category"],
                    record_data["activity_subtype"],
                    record_data["amount"],
                    record_data["unit"],
                    record_data["co2e_kg"],
                    record_data["date"]
                )
                result = execute_insert_returning(query, params)
                if result:
                    record = result
                else:
                    raise Exception("Insert returned no data")
            except Exception as e:
                print(f"Database error: {e}, falling back to in-memory")
                record = {
                    "id": f"act_{len(activities_db_fallback)}",
                    **record_data,
                    "created_at": datetime.now()
                }
                activities_db_fallback.append(record)
        else:
            record = {
                "id": f"act_{len(activities_db_fallback)}",
                **record_data,
                "created_at": datetime.now()
            }
            activities_db_fallback.append(record)
        
        return {
            "success": True,
            "emission_record": record,
            "message": f"Activity logged: {emission_result['co2e_kg']:.2f} kg CO₂e"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_activity_history(limit: int = 50):
    """Get activity history"""
    if has_database():
        try:
            query = """
                SELECT * FROM activities 
                ORDER BY created_at DESC 
                LIMIT %s
            """
            activities = execute_query(query, (limit,))
            
            # Get total count
            count_query = "SELECT COUNT(*) as total FROM activities"
            count_result = execute_query(count_query)
            total = count_result[0]["total"] if count_result else len(activities)
            
            return {
                "activities": activities,
                "total": total
            }
        except Exception as e:
            print(f"Database error: {e}, using fallback")
            return {
                "activities": activities_db_fallback[-limit:],
                "total": len(activities_db_fallback)
            }
    else:
        return {
            "activities": activities_db_fallback[-limit:],
            "total": len(activities_db_fallback)
        }

