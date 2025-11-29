"""
KMeans clustering service for user archetype classification
"""
import os
import pickle
import json
import numpy as np
from typing import Dict, Any, Optional
from sklearn.preprocessing import StandardScaler

import os
from pathlib import Path

# Get the project root directory (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "ml_services" / "models"

def load_kmeans_model():
    """Load trained KMeans model and scaler"""
    try:
        with open(f"{MODEL_DIR}/kmeans.pkl", "rb") as f:
            kmeans = pickle.load(f)
        
        with open(f"{MODEL_DIR}/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        
        with open(f"{MODEL_DIR}/cluster_descriptions.json", "r") as f:
            cluster_descriptions = json.load(f)
        
        return kmeans, scaler, cluster_descriptions
    except FileNotFoundError as e:
        print(f"Model files not found: {e}")
        print("Please run ml_services/train_kmeans.py first")
        return None, None, None

def classify_user_archetype(user_emission_data: Dict[str, float]) -> Optional[Dict[str, Any]]:
    """
    Classify user into emission archetype using KMeans
    
    Args:
        user_emission_data: Dictionary with user emission features:
            - daily_miles_driven
            - meat_meals_per_week
            - electricity_kwh_per_day
            - natural_gas_therms_per_month
            - flights_per_year
            - transport_emissions_kg
            - food_emissions_kg
            - energy_emissions_kg
    
    Returns:
        Dictionary with cluster_id, archetype, and description
    """
    kmeans, scaler, cluster_descriptions = load_kmeans_model()
    
    if kmeans is None:
        return None
    
    # Prepare feature vector (must match training features)
    feature_cols = [
        "daily_miles_driven",
        "meat_meals_per_week",
        "electricity_kwh_per_day",
        "natural_gas_therms_per_month",
        "flights_per_year",
        "transport_emissions_kg",
        "food_emissions_kg",
        "energy_emissions_kg",
    ]
    
    # Extract features (use 0.0 as default if missing)
    feature_vector = np.array([
        user_emission_data.get(col, 0.0) for col in feature_cols
    ]).reshape(1, -1)
    
    # Scale features
    feature_vector_scaled = scaler.transform(feature_vector)
    
    # Predict cluster
    cluster_id = int(kmeans.predict(feature_vector_scaled)[0])
    
    # Get cluster description
    cluster_info = cluster_descriptions.get(str(cluster_id), {})
    
    return {
        "cluster_id": cluster_id,
        "archetype": cluster_info.get("archetype", "Unknown"),
        "description": cluster_info,
        "cluster_stats": cluster_info.get("stats", {})
    }

def generate_rule_based_recommendations(
    user_emission_data: Dict[str, float],
    archetype: str
) -> list:
    """
    Generate rule-based recommendations based on user archetype and emission data
    
    Returns list of recommendation dictionaries
    """
    recommendations = []
    
    # High Transportation archetype
    if "Transportation" in archetype or user_emission_data.get("transport_emissions_kg", 0) > 2000:
        miles = user_emission_data.get("daily_miles_driven", 0)
        if miles > 30:
            savings = (miles - 25) * 0.411 * 7  # Weekly savings
            recommendations.append({
                "title": "Reduce Daily Driving",
                "description": f"Reduce driving by {miles - 25:.1f} miles/week",
                "estimated_savings_kg": savings,
                "category": "transportation",
                "priority": "high"
            })
    
    # High Food Emissions
    if "Food" in archetype or user_emission_data.get("food_emissions_kg", 0) > 1500:
        meat_meals = user_emission_data.get("meat_meals_per_week", 0)
        if meat_meals > 7:
            savings = (meat_meals - 5) * 3.5  # Weekly savings
            recommendations.append({
                "title": "Reduce Meat Consumption",
                "description": f"Replace {meat_meals - 5} meat meals per week with vegetarian options",
                "estimated_savings_kg": savings * 52,  # Annual
                "category": "food",
                "priority": "high"
            })
    
    # High Energy Usage
    if "Energy" in archetype or user_emission_data.get("energy_emissions_kg", 0) > 3000:
        electricity = user_emission_data.get("electricity_kwh_per_day", 0)
        if electricity > 30:
            savings = (electricity - 25) * 0.5 * 365  # Annual savings
            recommendations.append({
                "title": "Reduce Energy Consumption",
                "description": f"Reduce daily electricity usage by {electricity - 25:.1f} kWh",
                "estimated_savings_kg": savings,
                "category": "energy",
                "priority": "medium"
            })
    
    # Low Total Emissions - encourage maintenance
    if "Low" in archetype:
        recommendations.append({
            "title": "Maintain Low Emissions",
            "description": "You're doing great! Continue your sustainable habits.",
            "estimated_savings_kg": 0,
            "category": "general",
            "priority": "low"
        })
    
    # General recommendations if no specific ones
    if not recommendations:
        recommendations.append({
            "title": "Track Your Progress",
            "description": "Continue logging activities to get personalized recommendations",
            "estimated_savings_kg": 0,
            "category": "general",
            "priority": "low"
        })
    
    return recommendations

