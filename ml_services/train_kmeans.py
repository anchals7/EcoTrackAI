"""
Train KMeans clustering model on synthetic user data
Identifies user emission archetypes
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle
import json
import os

def load_synthetic_data(filename="synthetic_users.json"):
    """Load synthetic user data"""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Please run generate_synthetic_data.py first to create {filename}")
    
    df = pd.read_json(filename)
    return df

def prepare_features(df):
    """
    Prepare features for clustering
    We'll use normalized emission values to identify patterns
    """
    # Features to use for clustering
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
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, scaler, feature_cols

def train_kmeans(X, n_clusters=6, random_state=42):
    """Train KMeans model"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    kmeans.fit(X)
    return kmeans

def analyze_clusters(df, kmeans, feature_cols):
    """Analyze and describe each cluster"""
    df_clustered = df.copy()
    df_clustered['cluster'] = kmeans.labels_
    
    cluster_descriptions = {}
    
    for cluster_id in range(kmeans.n_clusters):
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]
        
        # Calculate cluster statistics
        stats = {
            "size": len(cluster_data),
            "avg_total_emissions": cluster_data['total_annual_emissions_kg'].mean(),
            "avg_daily_miles": cluster_data['daily_miles_driven'].mean(),
            "avg_meat_meals": cluster_data['meat_meals_per_week'].mean(),
            "avg_electricity": cluster_data['electricity_kwh_per_day'].mean(),
            "avg_flights": cluster_data['flights_per_year'].mean(),
        }
        
        # Determine archetype based on dominant emission source
        # Use mean ratios per user, not total sums (more accurate)
        transport_ratio = cluster_data['transport_emissions_kg'].mean() / cluster_data['total_annual_emissions_kg'].mean()
        food_ratio = cluster_data['food_emissions_kg'].mean() / cluster_data['total_annual_emissions_kg'].mean()
        energy_ratio = cluster_data['energy_emissions_kg'].mean() / cluster_data['total_annual_emissions_kg'].mean()
        flight_ratio = cluster_data['flight_emissions_kg'].mean() / cluster_data['total_annual_emissions_kg'].mean()
        
        # Find the dominant source (highest ratio)
        ratios = {
            "transport": transport_ratio,
            "food": food_ratio,
            "energy": energy_ratio,
            "flight": flight_ratio
        }
        dominant = max(ratios, key=ratios.get)
        dominant_ratio = ratios[dominant]
        
        # Classify based on dominant source and total emissions
        avg_total = cluster_data['total_annual_emissions_kg'].mean()
        avg_electricity = cluster_data['electricity_kwh_per_day'].mean()
        avg_meat = cluster_data['meat_meals_per_week'].mean()
        
        # More lenient thresholds - use relative dominance, not absolute thresholds
        if avg_total < 6000:  # Low emissions overall
            archetype = "Low Total Emissions"
        elif dominant == "transport" and transport_ratio > 0.30 and transport_ratio > energy_ratio * 1.1:
            # Transport is at least 30% and 10% more than energy
            archetype = "High Transportation"
        elif dominant == "food" and food_ratio > 0.20:
            # Food is at least 20%
            archetype = "High Food Emissions"
        elif dominant == "energy":
            # Differentiate energy clusters by other characteristics
            if avg_electricity > 100:  # Extreme energy usage
                archetype = "Very High Energy Usage"
            elif avg_meat > 8:  # High energy + high food
                archetype = "High Energy & Food Usage"
            elif avg_total < 12000:  # Moderate energy
                archetype = "Moderate Energy Usage"
            else:
                archetype = "High Energy Usage"
        elif dominant == "flight" and flight_ratio > 0.15:
            archetype = "High Flight Emissions"
        else:
            # Check if it's a mixed/balanced pattern
            if max(transport_ratio, food_ratio, energy_ratio) < 0.50:
                archetype = "Balanced Emissions"
            else:
                archetype = "High Energy Usage"
        
        cluster_descriptions[cluster_id] = {
            "archetype": archetype,
            "stats": stats,
            "transport_ratio": round(transport_ratio, 3),
            "food_ratio": round(food_ratio, 3),
            "energy_ratio": round(energy_ratio, 3),
            "flight_ratio": round(flight_ratio, 3),
            "dominant_source": dominant,
            "dominant_ratio": round(dominant_ratio, 3),
        }
    
    return cluster_descriptions

def save_model(kmeans, scaler, cluster_descriptions, model_dir="models"):
    """Save trained model and metadata"""
    os.makedirs(model_dir, exist_ok=True)
    
    # Save KMeans model
    with open(f"{model_dir}/kmeans.pkl", "wb") as f:
        pickle.dump(kmeans, f)
    
    # Save scaler
    with open(f"{model_dir}/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    # Save cluster descriptions
    with open(f"{model_dir}/cluster_descriptions.json", "w") as f:
        json.dump(cluster_descriptions, f, indent=2)
    
    print(f"✅ Saved model to {model_dir}/")
    print(f"📊 Cluster Archetypes:")
    for cluster_id, desc in cluster_descriptions.items():
        print(f"   Cluster {cluster_id}: {desc['archetype']} ({desc['stats']['size']} users)")

if __name__ == "__main__":
    print("🌱 Training KMeans clustering model...")
    
    # Load data
    df = load_synthetic_data()
    print(f"📊 Loaded {len(df)} users")
    
    # Prepare features
    X, scaler, feature_cols = prepare_features(df)
    print(f"🔢 Using {len(feature_cols)} features for clustering")
    
    # Train model
    kmeans = train_kmeans(X, n_clusters=6)
    print(f"✅ Trained KMeans with {kmeans.n_clusters} clusters")
    
    # Analyze clusters
    cluster_descriptions = analyze_clusters(df, kmeans, feature_cols)
    
    # Save model
    save_model(kmeans, scaler, cluster_descriptions)
    print("✅ Training complete!")

