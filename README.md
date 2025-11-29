# 🌱 EcoTrack AI

A personal carbon footprint tracker powered by AI and ML to help individuals track and reduce their carbon emissions.

## 🚀 Features

- **Natural Language Input**: Use Gemini AI to parse natural language activity descriptions
- **Activity Logging**: Log activities via dropdown or natural language input
- **Emissions Tracking**: Calculate CO₂ emissions using Climatiq API
- **ML Forecasting**: Predict future emissions using Prophet
- **User Archetypes**: KMeans clustering to identify emission behavior patterns
- **AI Recommendations**: Personalized reduction suggestions powered by Gemini

## 🛠️ Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- TanStack Query
- Recharts

### Backend
- FastAPI (Python)
- Supabase (PostgreSQL)
- Prophet (Time Series Forecasting)
- scikit-learn (KMeans Clustering)

### AI/ML Services
- Google Gemini API
- Climatiq API

## 📁 Project Structure

```
EcoTrackAI/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── ml_services/       # ML models and training scripts
└── README.md
```

## 🚦 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Supabase account (free tier)

### Environment Variables

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

#### Backend (.env)
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
GEMINI_API_KEY=your_gemini_api_key
CLIMATIQ_API_KEY=your_climatiq_api_key
DATABASE_URL=your_supabase_connection_string
```

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Run database migrations (if needed)
5. Generate synthetic data for ML training:
   ```bash
   cd ml_services
   python generate_synthetic_data.py
   python train_kmeans.py
   ```

6. Start the backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

7. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## 📝 MVP Roadmap

- [x] Project setup
- [x] Synthetic data generation
- [x] KMeans model training
- [x] Backend API endpoints
- [x] Gemini integration
- [x] Climatiq integration
- [x] Prophet forecasting
- [x] Frontend UI
- [x] Dashboard charts
- [x] Recommendations system

✅ **MVP Complete!** See `SETUP.md` for detailed setup instructions and `PROJECT_SUMMARY.md` for full feature overview.

## 🎨 Color Palette

- Ink Black: `#001514`
- White: `#FBFFFE`
- Dark Garnet: `#6B0504`
- Rust Brown: `#A3320B`
- Sunflower Gold: `#E6AF2E`

