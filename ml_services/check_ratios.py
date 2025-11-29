"""
Quick script to check emission ratios in synthetic data
"""
import pandas as pd
import json

df = pd.read_json("synthetic_users.json")

# Calculate ratios for each user
df['transport_ratio'] = df['transport_emissions_kg'] / df['total_annual_emissions_kg']
df['food_ratio'] = df['food_emissions_kg'] / df['total_annual_emissions_kg']
df['energy_ratio'] = df['energy_emissions_kg'] / df['total_annual_emissions_kg']
df['flight_ratio'] = df['flight_emissions_kg'] / df['total_annual_emissions_kg']

print("Average ratios across all users:")
print(f"  Transport: {df['transport_ratio'].mean():.3f}")
print(f"  Food: {df['food_ratio'].mean():.3f}")
print(f"  Energy: {df['energy_ratio'].mean():.3f}")
print(f"  Flight: {df['flight_ratio'].mean():.3f}")

print("\nUsers where transport is dominant (>0.4):", (df['transport_ratio'] > 0.4).sum())
print("Users where food is dominant (>0.3):", (df['food_ratio'] > 0.3).sum())
print("Users where energy is dominant (>0.4):", (df['energy_ratio'] > 0.4).sum())
print("Users where flight is dominant (>0.2):", (df['flight_ratio'] > 0.2).sum())

print("\nSample user with highest transport ratio:")
transport_dominant = df.loc[df['transport_ratio'].idxmax()]
print(f"  Transport ratio: {transport_dominant['transport_ratio']:.3f}")
print(f"  Daily miles: {transport_dominant['daily_miles_driven']:.1f}")
print(f"  Energy ratio: {transport_dominant['energy_ratio']:.3f}")

