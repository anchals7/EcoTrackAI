# 🌱 EcoTrack AI - Setup Guide

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **Supabase account** (free tier) - Optional for MVP (using in-memory storage for now)
- **API Keys:**
  - Google Gemini API key (free tier)
  - Climatiq API key

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
# Add your API keys:
# - GEMINI_API_KEY
# - CLIMATIQ_API_KEY

# Start the server
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### 2. ML Services Setup

```bash
cd ml_services

# Generate synthetic data for KMeans training
python generate_synthetic_data.py

# Train KMeans model
python train_kmeans.py
```

This will create:
- `synthetic_users.json` - Training data
- `models/kmeans.pkl` - Trained model
- `models/scaler.pkl` - Feature scaler
- `models/cluster_descriptions.json` - Cluster metadata

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies (already done if you used create-next-app)
npm install

# Create .env.local file (copy from .env.local.example)
# Set NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

The frontend will run on `http://localhost:3000`

## API Keys Setup

### Google Gemini API

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Climatiq API

1. Go to [Climatiq](https://www.climatiq.io/)
2. Sign up for free account
3. Get your API key from dashboard
4. Add to `backend/.env`:
   ```
   CLIMATIQ_API_KEY=your_api_key_here
   ```

## Project Structure

```
EcoTrackAI/
├── frontend/              # Next.js application
│   ├── app/              # App router pages
│   ├── lib/              # API client and utilities
│   └── ...
├── backend/              # FastAPI application
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic (Gemini, Climatiq, ML)
│   ├── models/          # Pydantic schemas
│   └── main.py          # FastAPI app entry point
└── ml_services/         # ML training scripts
    ├── generate_synthetic_data.py
    ├── train_kmeans.py
    └── models/          # Trained models
```

## Features

### ✅ Implemented

- [x] Natural language activity parsing (Gemini)
- [x] Dropdown-based activity logging
- [x] Emissions calculation (Climatiq + fallback)
- [x] Daily/weekly emissions tracking
- [x] Prophet forecasting (7-day predictions)
- [x] KMeans user archetype classification
- [x] LLM-enhanced recommendations
- [x] Dashboard with charts (Recharts)
- [x] Activity logging UI
- [x] Recommendations page

### 🔄 Future Enhancements

- [ ] User authentication (Supabase Auth)
- [ ] Database persistence (Supabase PostgreSQL)
- [ ] User profiles and settings
- [ ] Historical data visualization
- [ ] Export data functionality
- [ ] Mobile app
- [ ] Social features (leaderboards, challenges)

## Testing the MVP

1. **Start Backend**: `cd backend && uvicorn main:app --reload`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Train ML Models**: `cd ml_services && python generate_synthetic_data.py && python train_kmeans.py`
4. **Log Activities**: Go to `http://localhost:3000/log`
   - Try natural language: "I drove 10 miles today"
   - Or use dropdown form
5. **View Dashboard**: `http://localhost:3000/dashboard`
6. **Get Recommendations**: `http://localhost:3000/recommendations`

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure you're running from the `backend/` directory
- **API key errors**: Check `.env` file exists and has correct keys
- **Prophet errors**: May need to install additional dependencies (see requirements.txt)

### Frontend Issues

- **API connection errors**: Check `NEXT_PUBLIC_API_URL` in `.env.local`
- **Chart not rendering**: Make sure Recharts is installed (`npm install recharts`)

### ML Issues

- **Model not found**: Run `train_kmeans.py` first
- **Prophet forecast errors**: Need at least 7 days of activity data

## Color Palette

The app uses this custom color scheme:
- **Ink Black**: `#001514` - Primary text
- **White**: `#FBFFFE` - Background
- **Dark Garnet**: `#6B0504` - Accent/Highlights
- **Rust Brown**: `#A3320B` - Secondary accent
- **Sunflower Gold**: `#E6AF2E` - CTAs/Highlights

## Next Steps

1. Add more activity categories and subtypes
2. Improve Climatiq activity mapping
3. Add user authentication
4. Connect to Supabase database
5. Enhance recommendation algorithms
6. Add more visualization options

## License

This is an MVP project for portfolio/resume purposes.

