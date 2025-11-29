# 🌱 EcoTrack AI - Project Summary

## Overview

EcoTrack AI is a personal carbon footprint tracker that uses AI and ML to help individuals track and reduce their carbon emissions. The MVP is fully functional and ready for demonstration.

## Tech Stack

### Frontend
- **Next.js 14** (App Router) with TypeScript
- **Tailwind CSS** with custom color palette
- **TanStack Query** for data fetching
- **Recharts** for data visualization

### Backend
- **FastAPI** (Python) for REST API
- **Google Gemini API** for natural language processing
- **Climatiq API** for emissions calculations
- **Prophet** for time series forecasting
- **scikit-learn** (KMeans) for user clustering

### ML Services
- **Prophet** - 7-day emissions forecasting
- **KMeans Clustering** - User archetype classification (4 clusters)
- **Synthetic Data Generation** - Training data for ML models

## Key Features

### 1. Activity Logging
- **Natural Language Input**: Users can describe activities in plain English
  - Example: "I drove 10 miles to work today"
  - Gemini AI parses and extracts structured data
- **Dropdown Form**: Traditional form-based input for precise logging
- **Real-time Emissions Calculation**: Uses Climatiq API with fallback calculations

### 2. Emissions Tracking
- **Daily Summary**: Track emissions by day
- **Weekly Breakdown**: Category-wise weekly analysis
- **Historical Data**: View past emissions patterns

### 3. ML Forecasting
- **Prophet Model**: Predicts next 7 days of emissions
- **Trend Analysis**: Identifies increasing/decreasing/stable trends
- **Confidence Intervals**: Upper and lower bounds for predictions

### 4. User Archetypes
- **KMeans Clustering**: Classifies users into 4 archetypes:
  - High Transportation
  - High Food Emissions
  - High Energy Usage
  - Low Total Emissions
- **Behavioral Insights**: Based on emission patterns

### 5. AI Recommendations
- **Rule-based Logic**: Generates recommendations based on archetype
- **LLM Enhancement**: Gemini rephrases recommendations for better readability
- **Priority Levels**: High, medium, low priority recommendations
- **Savings Estimates**: Shows potential CO₂ savings

### 6. Dashboard
- **Summary Cards**: Total emissions, activities, categories
- **Daily Emissions Chart**: Bar chart showing daily breakdown
- **Category Pie Chart**: Visual breakdown by category
- **Forecast Line Chart**: 7-day prediction with confidence intervals

## Project Structure

```
EcoTrackAI/
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Home page
│   │   ├── dashboard/        # Dashboard with charts
│   │   ├── log/              # Activity logging
│   │   ├── recommendations/  # AI recommendations
│   │   └── layout.tsx        # Root layout
│   ├── lib/
│   │   ├── api.ts            # API client
│   │   └── queryClient.ts   # TanStack Query setup
│   └── tailwind.config.ts    # Custom colors
│
├── backend/
│   ├── routers/
│   │   ├── activities.py     # Activity logging endpoints
│   │   ├── emissions.py     # Emissions tracking endpoints
│   │   └── recommendations.py # Recommendations endpoint
│   ├── services/
│   │   ├── gemini_service.py  # Gemini AI integration
│   │   ├── climatiq_service.py # Climatiq API integration
│   │   ├── prophet_service.py # Prophet forecasting
│   │   └── kmeans_service.py # KMeans clustering
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   └── main.py              # FastAPI app
│
└── ml_services/
    ├── generate_synthetic_data.py # Generate training data
    ├── train_kmeans.py            # Train KMeans model
    └── models/                    # Trained models
        ├── kmeans.pkl
        ├── scaler.pkl
        └── cluster_descriptions.json
```

## API Endpoints

### Activities
- `POST /activity/log` - Log new activity
- `GET /activity/history` - Get activity history

### Emissions
- `GET /emissions/daily` - Get daily emissions
- `GET /emissions/weekly` - Get weekly emissions
- `GET /emissions/predict` - Get 7-day forecast
- `GET /emissions/summary` - Get overall summary

### Recommendations
- `GET /recommendations/` - Get personalized recommendations

## Color Palette

The app uses a custom, eco-friendly color scheme:
- **Ink Black** (`#001514`) - Primary text, headers
- **White** (`#FBFFFE`) - Background
- **Dark Garnet** (`#6B0504`) - Accents, high priority
- **Rust Brown** (`#A3320B`) - Secondary accents
- **Sunflower Gold** (`#E6AF2E`) - CTAs, highlights

## MVP Status

✅ **Complete Features:**
- Natural language activity parsing
- Dropdown activity logging
- Emissions calculation (Climatiq + fallback)
- Daily/weekly tracking
- Prophet forecasting
- KMeans user classification
- LLM-enhanced recommendations
- Full dashboard with charts
- Responsive UI

🔄 **Future Enhancements:**
- User authentication
- Database persistence (Supabase)
- User profiles
- Historical data export
- Mobile app
- Social features

## Getting Started

See `SETUP.md` for detailed setup instructions.

Quick start:
1. Install dependencies (backend + frontend)
2. Get API keys (Gemini, Climatiq)
3. Train ML models (`ml_services/train_kmeans.py`)
4. Start backend (`uvicorn main:app --reload`)
5. Start frontend (`npm run dev`)

## Demo Flow

1. **Log Activities**: Go to `/log` and log some activities
   - Try: "I drove 15 miles today"
   - Or use dropdown: Transportation → Car → 15 miles

2. **View Dashboard**: Go to `/dashboard` to see:
   - Daily emissions chart
   - Category breakdown
   - 7-day forecast

3. **Get Recommendations**: Go to `/recommendations` to see:
   - Your emission archetype
   - Personalized recommendations
   - Potential savings

## Resume Highlights

This project demonstrates:
- **Full-stack development** (Next.js + FastAPI)
- **AI/ML integration** (Gemini, Prophet, KMeans)
- **API integration** (Climatiq, Gemini)
- **Data visualization** (Recharts)
- **Modern React patterns** (TanStack Query, App Router)
- **TypeScript** for type safety
- **Clean architecture** (separation of concerns)

## Notes

- Currently uses in-memory storage (activities_db list)
- ML models are pre-trained on synthetic data
- Prophet requires 7+ days of data for forecasting
- All API keys should be stored in `.env` files (not committed)

## License

MVP project for portfolio/resume purposes.

