"""
Generate synthetic user data for KMeans clustering training
Creates realistic distributions of user emission behaviors
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def generate_synthetic_users(n_users=1000, seed=42):
    """
    Generate synthetic user data with realistic emission patterns
    
    Features:
    - daily_miles_driven: Normal distribution (mean=25, std=15)
    - meat_meals_per_week: Discrete uniform (0-14)
    - vegetarian_meals_per_week: Discrete uniform (0-14)
    - electricity_kwh_per_day: Log-normal distribution
    - natural_gas_therms_per_month: Log-normal distribution
    - flights_per_year: Highly skewed (most users have 0-2)
    """
    np.random.seed(seed)
    
    users = []
    
    for i in range(n_users):
        # Create diverse archetypes by varying distributions
        # 25% high transport, 25% high food, 25% high energy, 25% balanced/low
        archetype_type = np.random.choice([0, 1, 2, 3], p=[0.25, 0.25, 0.25, 0.25])
        
        if archetype_type == 0:  # High Transportation
            daily_miles = max(0, np.random.normal(45, 10))  # High miles
            meat_meals = np.random.randint(2, 8)  # Moderate food
            veg_meals = np.random.randint(2, 8)
            electricity_kwh = max(5, np.random.lognormal(3.2, 0.6))  # Lower energy
            gas_therms = max(0, np.random.lognormal(2.0, 0.8))
        elif archetype_type == 1:  # High Food Emissions
            daily_miles = max(0, np.random.normal(15, 8))  # Lower transport
            meat_meals = np.random.randint(8, 15)  # High meat consumption
            veg_meals = np.random.randint(0, 5)
            electricity_kwh = max(5, np.random.lognormal(3.3, 0.7))
            gas_therms = max(0, np.random.lognormal(2.2, 0.9))
        elif archetype_type == 2:  # High Energy Usage
            daily_miles = max(0, np.random.normal(20, 10))  # Moderate transport
            meat_meals = np.random.randint(3, 10)
            veg_meals = np.random.randint(3, 10)
            electricity_kwh = max(10, np.random.lognormal(4.0, 0.8))  # High energy
            gas_therms = max(5, np.random.lognormal(3.0, 1.0))
        else:  # Balanced/Low Emissions
            daily_miles = max(0, np.random.normal(15, 8))  # Lower miles
            meat_meals = np.random.randint(0, 6)  # Lower meat
            veg_meals = np.random.randint(5, 15)  # More vegetarian
            electricity_kwh = max(5, np.random.lognormal(3.0, 0.6))  # Lower energy
            gas_therms = max(0, np.random.lognormal(1.8, 0.7))
        
        # Flights - highly skewed (most people don't fly much)
        flights = np.random.choice(
            [0, 0, 0, 0, 0, 1, 1, 2, 3, 5, 10],  # Weighted towards 0
            p=[0.4, 0.2, 0.1, 0.05, 0.05, 0.1, 0.05, 0.02, 0.02, 0.005, 0.005]
        )
        
        # Calculate approximate total annual emissions (rough estimates)
        # These are simplified calculations for clustering purposes
        transport_emissions = daily_miles * 365 * 0.411  # kg CO2 per mile (average car) - annual
        food_emissions = (meat_meals * 3.5 + veg_meals * 0.5) * 52  # kg CO2 per meal - annual (weekly * 52)
        # Energy: electricity is daily, gas is monthly
        energy_emissions = (electricity_kwh * 0.5 * 365) + (gas_therms * 5.3 * 12)  # kg CO2 - annual
        flight_emissions = flights * 900  # kg CO2 per flight (average) - annual
        
        total_annual_emissions = (
            transport_emissions + 
            food_emissions + 
            energy_emissions + 
            flight_emissions
        )
        
        user = {
            "user_id": f"user_{i:04d}",
            "daily_miles_driven": round(daily_miles, 2),
            "meat_meals_per_week": meat_meals,
            "vegetarian_meals_per_week": veg_meals,
            "electricity_kwh_per_day": round(electricity_kwh, 2),
            "natural_gas_therms_per_month": round(gas_therms, 2),
            "flights_per_year": flights,
            "total_annual_emissions_kg": round(total_annual_emissions, 2),
            "transport_emissions_kg": round(transport_emissions, 2),
            "food_emissions_kg": round(food_emissions, 2),
            "energy_emissions_kg": round(energy_emissions, 2),
            "flight_emissions_kg": round(flight_emissions, 2),
        }
        
        users.append(user)
    
    return pd.DataFrame(users)

def save_synthetic_data(df, filename="synthetic_users.json"):
    """Save synthetic data to JSON file"""
    df.to_json(filename, orient="records", indent=2)
    print(f"✅ Saved {len(df)} synthetic users to {filename}")
    print(f"📊 Statistics:")
    print(f"   Total emissions range: {df['total_annual_emissions_kg'].min():.2f} - {df['total_annual_emissions_kg'].max():.2f} kg CO2/year")
    print(f"   Average emissions: {df['total_annual_emissions_kg'].mean():.2f} kg CO2/year")
    print(f"   Median emissions: {df['total_annual_emissions_kg'].median():.2f} kg CO2/year")

if __name__ == "__main__":
    print("🌱 Generating synthetic user data for KMeans training...")
    df = generate_synthetic_users(n_users=1000)
    save_synthetic_data(df)
    print("✅ Done!")

