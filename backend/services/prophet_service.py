"""
Prophet time series forecasting service
"""
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np

# Try to import Prophet with cmdstanpy backend
PROPHET_AVAILABLE = False
Prophet = None

try:
    from prophet import Prophet
    # Check if Prophet can actually initialize (requires cmdstanpy)
    try:
        # Try to create a minimal Prophet instance to test
        test_model = Prophet()
        PROPHET_AVAILABLE = True
        del test_model  # Clean up
    except (AttributeError, Exception) as e:
        # Prophet installed but backend not working
        PROPHET_AVAILABLE = False
        print(f"⚠️  Prophet installed but backend not available: {e}")
        print("⚠️  Will use simple forecast fallback")
except ImportError:
    # Prophet not installed at all
    PROPHET_AVAILABLE = False
    print("⚠️  Prophet not installed. Using simple forecast fallback")

def generate_forecast(
    historical_data: List[Dict[str, Any]],
    days_ahead: int = 7
) -> Dict[str, Any]:
    """
    Generate emissions forecast using Prophet
    
    Args:
        historical_data: List of dicts with 'date' and 'total_emissions' keys
        days_ahead: Number of days to forecast
    
    Returns:
        Dictionary with predictions and trend analysis
    """
    if len(historical_data) < 7:
        # Not enough data for reliable forecast
        return {
            "predictions": [],
            "next_7_days_total": 0.0,
            "trend": "insufficient_data",
            "message": "Need at least 7 days of data for forecasting"
        }
    
    # Prepare DataFrame for Prophet
    df = pd.DataFrame(historical_data)
    df['ds'] = pd.to_datetime(df['date'])
    df['y'] = df['total_emissions']
    df = df[['ds', 'y']].sort_values('ds')
    
    # Check if Prophet is available
    if not PROPHET_AVAILABLE or Prophet is None:
        return generate_simple_forecast(historical_data, days_ahead)
    
    # Initialize and fit Prophet model
    try:
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False,
            changepoint_prior_scale=0.05
        )
        model.fit(df)
    except (AttributeError, ImportError, Exception) as prophet_error:
        # Prophet initialization failed (common on Windows)
        print(f"⚠️  Prophet initialization failed: {prophet_error}")
        print("⚠️  Using simple forecast fallback")
        return generate_simple_forecast(historical_data, days_ahead)
    
    try:
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=days_ahead)
        forecast = model.predict(future)
        
        # Extract predictions for next N days
        future_forecast = forecast.tail(days_ahead)
        
        predictions = []
        for _, row in future_forecast.iterrows():
            predictions.append({
                "date": row['ds'].strftime("%Y-%m-%d"),
                "predicted_emissions_kg": max(0, row['yhat']),  # Ensure non-negative
                "lower_bound_kg": max(0, row['yhat_lower']),
                "upper_bound_kg": max(0, row['yhat_upper'])
            })
        
        # Calculate trend
        recent_avg = df.tail(7)['y'].mean()
        predicted_avg = future_forecast['yhat'].mean()
        
        if predicted_avg > recent_avg * 1.1:
            trend = "increasing"
        elif predicted_avg < recent_avg * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "predictions": predictions,
            "next_7_days_total": float(future_forecast['yhat'].sum()),
            "trend": trend,
            "recent_average": float(recent_avg),
            "predicted_average": float(predicted_avg)
        }
    
    except Exception as e:
        print(f"⚠️  Error generating Prophet forecast: {e}")
        print("⚠️  Using simple forecast fallback")
        # Fallback: simple linear projection
        return generate_simple_forecast(historical_data, days_ahead)

def generate_simple_forecast(
    historical_data: List[Dict[str, Any]],
    days_ahead: int = 7
) -> Dict[str, Any]:
    """
    Simple linear forecast fallback
    """
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    recent_avg = df.tail(7)['total_emissions'].mean()
    
    predictions = []
    last_date = df['date'].max()
    
    for i in range(1, days_ahead + 1):
        future_date = last_date + timedelta(days=i)
        predictions.append({
            "date": future_date.strftime("%Y-%m-%d"),
            "predicted_emissions_kg": recent_avg,
            "lower_bound_kg": recent_avg * 0.8,
            "upper_bound_kg": recent_avg * 1.2
        })
    
    return {
        "predictions": predictions,
        "next_7_days_total": recent_avg * days_ahead,
        "trend": "stable",
        "recent_average": float(recent_avg)
    }

