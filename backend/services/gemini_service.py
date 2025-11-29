"""
Gemini AI service for natural language parsing
"""
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import google.generativeai as genai
from typing import Optional
from models.schemas import ActivityStructured
import json

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_model():
    """Get available Gemini model (tries latest stable models first)"""
    # Try models in order: latest stable first, then preview/experimental
    model_names = [
        'gemini-2.5-flash',           # Latest stable flash (fast, free tier)
        'gemini-2.5-pro',             # Latest stable pro (more capable)
        'gemini-2.0-flash',           # Stable flash
        'gemini-flash-latest',        # Latest flash alias
        'gemini-pro-latest',          # Latest pro alias
        'gemini-2.0-flash-exp',        # Experimental flash
        'gemini-2.5-pro-preview-06-05',  # Preview pro
        'gemini-1.5-flash',           # Older stable
        'gemini-1.5-pro',             # Older stable
        'gemini-pro'                  # Legacy
    ]
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test if model is accessible by trying to generate (lightweight check)
            return model
        except Exception as e:
            continue
    
    raise ValueError("No available Gemini model found. Check your API key and model access.")

def parse_activity_text(text: str) -> Optional[ActivityStructured]:
    """
    Parse natural language activity description into structured format
    
    Example input: "I drove 10 miles to work today"
    Example output: {
        "category": "transportation",
        "subtype": "car",
        "amount": 10,
        "unit": "miles",
        "description": "Drove to work"
    }
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not configured")
    
    try:
        model = get_gemini_model()
        
        prompt = f"""
Parse the following activity description into structured JSON format.
Extract: category, subtype, amount, unit, and a brief description.

Activity description: "{text}"

Return ONLY valid JSON in this exact format:
{{
    "category": "transportation|food|energy|waste|other",
    "subtype": "specific activity type (e.g., car, beef, electricity)",
    "amount": <number>,
    "unit": "miles|kg|kwh|therms|etc",
    "description": "brief description"
}}

If the amount cannot be determined, use 1.0 as default.
If the unit cannot be determined, infer from context or use "unit".
"""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        data = json.loads(response_text)
        
        return ActivityStructured(
            category=data.get("category", "other"),
            subtype=data.get("subtype", "unknown"),
            amount=float(data.get("amount", 1.0)),
            unit=data.get("unit", "unit"),
            description=data.get("description", text)
        )
    
    except Exception as e:
        print(f"Error parsing activity with Gemini: {e}")
        return None

def generate_recommendation_text(rule_based_recommendation: str) -> str:
    """
    Enhance rule-based recommendations with LLM for better readability
    
    Example input: "Reduce driving by 10 miles/week to lower emissions by 2.3 kg CO2"
    Example output: "You can significantly reduce your carbon impact by slightly adjusting 
                     travel habits. Cutting just 10 miles of driving per week lowers your 
                     footprint by roughly 2.3 kg CO₂ — about the same impact as skipping a beef meal."
    """
    if not GEMINI_API_KEY:
        return rule_based_recommendation
    
    try:
        model = get_gemini_model()
        
        prompt = f"""
Rewrite this carbon reduction recommendation in a friendly, encouraging, and engaging way.
Keep the key information (numbers, actions) but make it more conversational and motivating.

Original recommendation: "{rule_based_recommendation}"

Return only the rewritten recommendation text, nothing else.
"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error generating recommendation text with Gemini: {e}")
        return rule_based_recommendation
