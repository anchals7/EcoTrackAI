# EcoTrack AI - Developer Documentation

This file contains technical setup and development information. For project overview, see [README.md](README.md).

## 🌱 Project Overview

EcoTrack AI is a personal carbon footprint tracker that combines AI/ML technologies to help users understand and reduce their environmental impact.

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query
- **Charts**: Recharts

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **API Integration**: 
  - Google Gemini API (natural language processing)
  - Climatiq API (emissions calculations)

### ML/AI Services
- **Prophet**: Time-series forecasting for emissions predictions
- **scikit-learn**: KMeans clustering for user archetype classification
- **Google Gemini**: Natural language parsing and recommendation enhancement

## 📁 Project Structure

```
EcoTrackAI/
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend
│   ├── routers/       # API endpoints
│   ├── services/      # Business logic (Gemini, Climatiq, Prophet, KMeans)
│   ├── models/        # Pydantic schemas
│   └── database/      # Database schema and setup
├── ml_services/       # ML model training scripts
│   └── models/        # Trained KMeans model
└── README.md          # Project overview
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- Supabase account (or PostgreSQL database)
- API Keys:
  - Google Gemini API key
  - Climatiq API key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `env.example` to `.env`
   - Fill in your API keys and database URL
   - See `ENV_SETUP.md` for detailed instructions

5. **Set up database:**
   - Run the SQL script in `database/schema.sql` in your Supabase SQL editor
   - See `DATABASE_SETUP.md` for detailed instructions

6. **Start the backend server:**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env.local`
   - Set `NEXT_PUBLIC_API_URL=http://localhost:8000`

4. **Start the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

### ML Services Setup

1. **Navigate to ml_services directory:**
   ```bash
   cd ml_services
   ```

2. **Generate synthetic training data:**
   ```bash
   python generate_synthetic_data.py
   ```

3. **Train KMeans model:**
   ```bash
   python train_kmeans.py
   ```

4. **Optional: Install Prophet for forecasting:**
   - See `PROPHET_SETUP.md` for Windows-specific instructions
   - The system gracefully falls back to simple forecasting if Prophet is unavailable

## 🎨 Custom Color Palette

The project uses a custom color scheme:
- **Ink Black**: `#001514`
- **White**: `#FBFFFE`
- **Dark Garnet**: `#6B0504`
- **Rust Brown**: `#A3320B`
- **Sunflower Gold**: `#E6AF2E`

## 📊 API Endpoints

### Activities
- `POST /activity/log` - Log a new activity (supports natural language or structured input)
- `GET /activity/history` - Get activity history

### Emissions
- `GET /emissions/daily` - Get daily emissions breakdown
- `GET /emissions/weekly` - Get weekly emissions summary
- `GET /emissions/predict?days_ahead=7` - Get emissions forecast

### Recommendations
- `GET /recommendations/` - Get personalized recommendations based on user archetype

## 🤖 ML Features

### KMeans Clustering
- Trained on synthetic user data
- Classifies users into emission archetypes (e.g., "High Transportation", "Energy-Conscious")
- Model saved in `ml_services/models/kmeans_model.pkl`

### Prophet Forecasting
- Time-series forecasting for emissions predictions
- Requires at least 7 days of historical data
- Falls back to simple statistical forecast if Prophet unavailable

### Natural Language Processing
- Gemini AI parses natural language activity descriptions
- Extracts: category, subtype, amount, unit
- Falls back to heuristic parsing if Gemini unavailable

## 🧪 Testing

### Test Natural Language Logging
```bash
curl -X POST http://localhost:8000/activity/log \
  -H "Content-Type: application/json" \
  -d '{"text": "I drove 15 miles to work today"}'
```

### Test Structured Logging
```bash
curl -X POST http://localhost:8000/activity/log \
  -H "Content-Type: application/json" \
  -d '{
    "category": "transportation",
    "subtype": "car",
    "amount": 15,
    "unit": "miles"
  }'
```

## 📝 Environment Variables

### Backend (.env)
- `GEMINI_API_KEY` - Google Gemini API key
- `CLIMATIQ_API_KEY` - Climatiq API key
- `DATABASE_URL` - Supabase PostgreSQL connection string
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `ENVIRONMENT` - Development/Production

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL

## 🐛 Troubleshooting

### Prophet Installation Issues (Windows)
- See `PROPHET_SETUP.md` for detailed setup
- The system works fine with the simple forecast fallback

### Database Connection Issues
- Verify `DATABASE_URL` is correctly formatted
- Check Supabase connection settings
- System falls back to in-memory storage if database unavailable

### Gemini API Errors
- Run `python backend/list_gemini_models.py` to see available models
- Update model names in `backend/services/gemini_service.py` if needed

## 📚 Additional Documentation

- `ENV_SETUP.md` - Detailed environment variable setup
- `DATABASE_SETUP.md` - Supabase database setup guide
- `PROPHET_SETUP.md` - Prophet installation guide (Windows)
- `README.md` - Project overview and features

## 🚧 MVP Roadmap

### Phase 1: Data & ML Foundations ✅
- [x] Synthetic data generation
- [x] KMeans model training
- [x] Prophet forecasting setup

### Phase 2: Backend Services ✅
- [x] FastAPI backend
- [x] Activity logging (NL + structured)
- [x] Emissions calculations
- [x] Forecasting endpoint
- [x] Recommendations endpoint

### Phase 3: Frontend ✅
- [x] Activity logging UI
- [x] Dashboard with charts
- [x] Recommendations page

### Phase 4: Future Enhancements
- [ ] User authentication
- [ ] Multi-user support
- [ ] Export data functionality
- [ ] Mobile app
- [ ] Social sharing features

