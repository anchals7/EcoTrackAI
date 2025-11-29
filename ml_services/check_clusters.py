"""
Check what makes each cluster different
"""
import pandas as pd
import pickle
import json
from sklearn.preprocessing import StandardScaler

# Load data and model
df = pd.read_json("synthetic_users.json")
with open("models/kmeans.pkl", "rb") as f:
    kmeans = pickle.load(f)
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("models/cluster_descriptions.json", "r") as f:
    descriptions = json.load(f)

# Prepare features
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
X = df[feature_cols].values
X_scaled = scaler.transform(X)
df['cluster'] = kmeans.labels_

print("Cluster Analysis:\n")
for cluster_id in range(kmeans.n_clusters):
    cluster_data = df[df['cluster'] == cluster_id]
    desc = descriptions.get(str(cluster_id), {})
    
    print(f"Cluster {cluster_id}: {desc.get('archetype', 'Unknown')} ({len(cluster_data)} users)")
    print(f"  Avg daily miles: {cluster_data['daily_miles_driven'].mean():.1f}")
    print(f"  Avg meat meals/week: {cluster_data['meat_meals_per_week'].mean():.1f}")
    print(f"  Avg electricity kWh/day: {cluster_data['electricity_kwh_per_day'].mean():.1f}")
    print(f"  Avg total emissions: {cluster_data['total_annual_emissions_kg'].mean():.0f} kg/year")
    print(f"  Transport ratio: {desc.get('transport_ratio', 0):.3f}")
    print(f"  Food ratio: {desc.get('food_ratio', 0):.3f}")
    print(f"  Energy ratio: {desc.get('energy_ratio', 0):.3f}")
    print()

