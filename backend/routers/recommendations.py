"""
Recommendations endpoint
"""
from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from models.schemas import RecommendationsResponse, Recommendation
from services.kmeans_service import classify_user_archetype, generate_rule_based_recommendations
from services.gemini_service import generate_recommendation_text
from collections import defaultdict
from datetime import datetime, timedelta, timezone
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

@router.get("/")
async def get_recommendations():
    """
    Get personalized recommendations based on user archetype and emissions
    """
    all_activities = get_activities()
    
    if not all_activities:
        return {
            "user_archetype": "Unknown",
            "recommendations": [{
                "title": "Start Logging Activities",
                "description": "Begin logging your daily activities to receive personalized recommendations.",
                "estimated_savings_kg": 0,
                "category": "general",
                "priority": "low"
            }],
            "total_potential_savings_kg": 0
        }
    
    # Calculate user emission statistics (last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    recent_activities = []
    for act in all_activities:
        act_date = act.get("date")
        if act_date:
            if isinstance(act_date, str):
                # Handle both timezone-aware and naive strings
                if act_date.endswith('Z') or '+' in act_date or act_date.count('-') > 2:
                    act_date = datetime.fromisoformat(act_date.replace('Z', '+00:00'))
                else:
                    act_date = datetime.fromisoformat(act_date)
                    # Make it timezone-aware if it's naive
                    if act_date.tzinfo is None:
                        act_date = act_date.replace(tzinfo=timezone.utc)
            elif isinstance(act_date, datetime):
                # Make timezone-aware if naive
                if act_date.tzinfo is None:
                    act_date = act_date.replace(tzinfo=timezone.utc)
            
            if isinstance(act_date, datetime) and act_date >= thirty_days_ago:
                recent_activities.append(act)
    
    # Aggregate emission data for KMeans classification
    daily_miles = 0
    meat_meals = 0
    veg_meals = 0
    electricity_kwh = 0
    gas_therms = 0
    flights = 0
    
    transport_emissions = 0
    food_emissions = 0
    energy_emissions = 0
    
    for act in recent_activities:
        category = act.get("activity_category", "")
        emissions = float(act.get("co2e_kg", 0))
        unit = act.get("unit", "").lower()
        subtype = act.get("activity_subtype", "").lower()
        amount = float(act.get("amount", 0))
        
        if category == "transportation":
            transport_emissions += emissions
            if unit in ["miles", "km"]:
                daily_miles += amount / 30  # Average daily
        elif category == "food":
            food_emissions += emissions
            if "meat" in subtype or "beef" in subtype:
                meat_meals += 1
            else:
                veg_meals += 1
        elif category == "energy":
            energy_emissions += emissions
            if unit in ["kwh", "kilowatt-hour"]:
                electricity_kwh += amount / 30  # Average daily
            elif "therm" in unit:
                gas_therms += amount / 30  # Average monthly
    
    # Prepare user emission data for classification
    user_emission_data = {
        "daily_miles_driven": daily_miles,
        "meat_meals_per_week": (meat_meals / 30) * 7,
        "vegetarian_meals_per_week": (veg_meals / 30) * 7,
        "electricity_kwh_per_day": electricity_kwh,
        "natural_gas_therms_per_month": gas_therms * 30,
        "flights_per_year": flights * 12,  # Rough estimate
        "transport_emissions_kg": transport_emissions * 365 / 30,  # Annualize
        "food_emissions_kg": food_emissions * 365 / 30,
        "energy_emissions_kg": energy_emissions * 365 / 30,
    }
    
    # Classify user archetype
    archetype_result = classify_user_archetype(user_emission_data)
    
    if archetype_result:
        archetype = archetype_result["archetype"]
    else:
        archetype = "Unknown"
    
    # Generate rule-based recommendations
    rule_recommendations = generate_rule_based_recommendations(user_emission_data, archetype)
    
    # Enhance recommendations with LLM
    enhanced_recommendations = []
    for rec in rule_recommendations:
        enhanced_description = generate_recommendation_text(
            f"{rec['title']}: {rec['description']}"
        )
        
        enhanced_recommendations.append(Recommendation(
            title=rec["title"],
            description=enhanced_description,
            estimated_savings_kg=rec["estimated_savings_kg"],
            category=rec["category"],
            priority=rec["priority"]
        ))
    
    total_savings = sum(rec.estimated_savings_kg for rec in enhanced_recommendations)
    
    return RecommendationsResponse(
        user_archetype=archetype,
        recommendations=enhanced_recommendations,
        total_potential_savings_kg=total_savings
    )

