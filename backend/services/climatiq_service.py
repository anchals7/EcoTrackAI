"""
Climatiq API service for emissions calculations
"""
import os
import requests
from typing import Optional, Dict, Any

CLIMATIQ_API_KEY = os.getenv("CLIMATIQ_API_KEY")
CLIMATIQ_BASE_URL = "https://beta3.api.climatiq.io"

def calculate_emissions(
    category: str,
    subtype: str,
    amount: float,
    unit: str
) -> Optional[Dict[str, Any]]:
    """
    Calculate CO2e emissions using Climatiq API
    
    Args:
        category: Activity category (transportation, food, energy, etc.)
        subtype: Specific activity (car, beef, electricity, etc.)
        amount: Amount of activity
        unit: Unit of measurement
    
    Returns:
        Dictionary with co2e_kg and other emission data
    """
    if not CLIMATIQ_API_KEY:
        raise ValueError("CLIMATIQ_API_KEY not configured")
    
    # Map our categories/subtypes to Climatiq activity IDs
    activity_id = map_to_climatiq_activity(category, subtype, unit)
    
    if not activity_id:
        # Fallback to default calculation if mapping not found
        return calculate_fallback_emissions(category, subtype, amount, unit)
    
    try:
        headers = {
            "Authorization": f"Bearer {CLIMATIQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "emission_factor": {
                "activity_id": activity_id
            },
            "parameters": {
                "money": None,
                "money_unit": None,
                "distance": None,
                "distance_unit": None,
                "weight": None,
                "weight_unit": None,
                "volume": None,
                "volume_unit": None,
                "energy": None,
                "energy_unit": None,
            }
        }
        
        # Set appropriate parameter based on unit
        if unit.lower() in ["miles", "km", "kilometers"]:
            distance_km = amount if unit.lower() in ["km", "kilometers"] else amount * 1.60934
            payload["parameters"]["distance"] = distance_km
            payload["parameters"]["distance_unit"] = "km"
        elif unit.lower() in ["kwh", "kilowatt-hour", "kilowatt-hours"]:
            payload["parameters"]["energy"] = amount
            payload["parameters"]["energy_unit"] = "kWh"
        elif unit.lower() in ["kg", "kilograms", "lbs", "pounds"]:
            weight_kg = amount if unit.lower() in ["kg", "kilograms"] else amount * 0.453592
            payload["parameters"]["weight"] = weight_kg
            payload["parameters"]["weight_unit"] = "kg"
        
        response = requests.post(
            f"{CLIMATIQ_BASE_URL}/estimate",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            co2e_kg = data.get("co2e", 0) / 1000  # Convert to kg
            return {
                "co2e_kg": co2e_kg,
                "co2e": data.get("co2e", 0),
                "co2e_unit": "kg",
                "source": "climatiq"
            }
        else:
            print(f"Climatiq API error: {response.status_code} - {response.text}")
            return calculate_fallback_emissions(category, subtype, amount, unit)
    
    except Exception as e:
        print(f"Error calling Climatiq API: {e}")
        return calculate_fallback_emissions(category, subtype, amount, unit)

def map_to_climatiq_activity(category: str, subtype: str, unit: str) -> Optional[str]:
    """
    Map our activity categories to Climatiq activity IDs
    This is a simplified mapping - you may need to expand this
    """
    mapping = {
        ("transportation", "car", "miles"): "passenger_vehicle-vehicle_type_car-fuel_source_na-distance_na-engine_size_na",
        ("transportation", "car", "km"): "passenger_vehicle-vehicle_type_car-fuel_source_na-distance_na-engine_size_na",
        ("food", "beef", "kg"): "food-beef",
        ("food", "beef", "lbs"): "food-beef",
        ("energy", "electricity", "kwh"): "electricity-energy_source_grid_mix",
        ("energy", "electricity", "kilowatt-hour"): "electricity-energy_source_grid_mix",
    }
    
    return mapping.get((category.lower(), subtype.lower(), unit.lower()))

def calculate_fallback_emissions(
    category: str,
    subtype: str,
    amount: float,
    unit: str
) -> Dict[str, Any]:
    """
    Fallback emission calculations when Climatiq API is unavailable
    Uses simplified emission factors
    """
    # Simplified emission factors (kg CO2e per unit)
    factors = {
        ("transportation", "car", "miles"): 0.411,  # kg CO2e per mile
        ("transportation", "car", "km"): 0.255,     # kg CO2e per km
        ("food", "beef", "kg"): 27.0,                # kg CO2e per kg beef
        ("food", "beef", "lbs"): 12.25,             # kg CO2e per lb beef
        ("food", "chicken", "kg"): 6.9,
        ("food", "pork", "kg"): 12.1,
        ("energy", "electricity", "kwh"): 0.5,      # kg CO2e per kWh (US average)
        ("energy", "natural_gas", "therms"): 5.3,  # kg CO2e per therm
    }
    
    key = (category.lower(), subtype.lower(), unit.lower())
    factor = factors.get(key, 1.0)  # Default factor if not found
    
    co2e_kg = amount * factor
    
    return {
        "co2e_kg": co2e_kg,
        "co2e": co2e_kg * 1000,
        "co2e_unit": "kg",
        "source": "fallback"
    }

