# 🌱 EcoTrack AI

> **AI-powered personal carbon footprint tracker** that helps you understand and reduce your environmental impact through intelligent insights, natural language logging, and personalized recommendations.

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)

---

## 🎯 Why EcoTrack AI?

Climate change is one of the most pressing challenges of our time, yet many of us struggle to understand our personal contribution to carbon emissions. **EcoTrack AI** bridges this gap by combining cutting-edge AI and machine learning to make carbon tracking intuitive, insightful, and actionable.

### The Problem
- Most people don't know their carbon footprint
- Tracking emissions manually is tedious and error-prone
- Generic advice doesn't account for individual lifestyles
- Lack of motivation without seeing progress and predictions

### Our Solution
EcoTrack AI transforms carbon tracking from a chore into an engaging, personalized experience:
- **Natural Language Logging**: Just type "I drove 10 miles today" and let AI do the rest
- **Intelligent Insights**: ML-powered archetype classification reveals your emission patterns
- **Predictive Analytics**: See your future footprint with time-series forecasting
- **Personalized Recommendations**: Get tailored advice based on your unique lifestyle

---

## ✨ Key Features

### 🤖 AI-Powered Natural Language Processing
Log activities in plain English. Our Gemini AI integration understands context and extracts structured data automatically.

```
"I drove 15 miles to work and ate beef for lunch"
→ Automatically parsed and logged with accurate emissions calculations
```

### 📊 Real-Time Dashboard
Visualize your carbon footprint with interactive charts:
- Daily and weekly emissions breakdown
- Category-wise analysis (transportation, food, energy)
- Trend analysis and progress tracking

### 🔮 Predictive Forecasting
Powered by Prophet (Facebook's time-series forecasting library), predict your emissions for the next 7 days based on historical patterns.

### 🎯 Personalized Recommendations
Our KMeans clustering algorithm classifies you into emission archetypes (e.g., "High Transportation", "Energy-Conscious", "Frequent Flyer") and provides tailored reduction strategies enhanced by AI-generated, friendly explanations.

### 📱 Modern, Intuitive UI
Built with Next.js 14 and Tailwind CSS, featuring a custom color palette designed for clarity and engagement.

---

## 🎥 Demo Video

**Watch the full demo:** [Link to your demo video]

*See EcoTrack AI in action: natural language logging, real-time dashboard updates, forecasting, and personalized recommendations.*

---

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** (App Router) - Modern React framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **TanStack Query** - Server state management
- **Recharts** - Beautiful, responsive charts

### Backend
- **FastAPI** - High-performance Python web framework
- **Supabase (PostgreSQL)** - Scalable cloud database
- **Google Gemini API** - Natural language understanding
- **Climatiq API** - Accurate emissions calculations

### Machine Learning
- **Prophet** - Time-series forecasting for emissions predictions
- **scikit-learn (KMeans)** - User behavior clustering and archetype classification
- **Pandas & NumPy** - Data processing and analysis

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Supabase account
- API keys (Gemini, Climatiq)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EcoTrackAI.git
   cd EcoTrackAI
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env with your API keys
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Set NEXT_PUBLIC_API_URL=http://localhost:8000
   npm run dev
   ```

4. **Open your browser**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

For detailed setup instructions, see [DEVELOPER.md](DEVELOPER.md).

---

## 💡 How It Works

### 1. Log Activities
Users can log activities in two ways:
- **Natural Language**: "I drove 20 miles today"
- **Structured Input**: Select category, type, amount, and unit from dropdowns

### 2. AI Processing
- Gemini AI parses natural language into structured data
- Climatiq API calculates accurate CO₂e emissions
- Data is stored in Supabase PostgreSQL database

### 3. ML Analysis
- KMeans clustering analyzes user behavior patterns
- Classifies user into emission archetype
- Prophet forecasting predicts future emissions

### 4. Personalized Insights
- Dashboard visualizes emissions trends
- Recommendations engine suggests tailored reductions
- AI enhances recommendations with friendly, motivating language

---

## 🎨 Design Philosophy

EcoTrack AI is built with **clarity, simplicity, and impact** in mind:

- **Accessible**: Natural language input removes barriers to entry
- **Visual**: Charts and graphs make data digestible
- **Actionable**: Recommendations are specific and achievable
- **Motivating**: Progress tracking and predictions encourage continued use

---

## 📈 Project Status

This is an **MVP (Minimum Viable Product)** built to demonstrate:
- Full-stack development capabilities
- AI/ML integration in production applications
- Modern web development best practices
- End-to-end feature implementation

### Completed Features ✅
- Natural language activity logging
- Real-time emissions dashboard
- Time-series forecasting
- User archetype classification
- Personalized recommendations
- Responsive, modern UI

### Future Enhancements 🚧
- User authentication and multi-user support
- Mobile application
- Social sharing and community features
- Advanced analytics and insights
- Carbon offset integration

---

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@anchals7](https://github.com/anchals7)
- LinkedIn: [anchal-developer](https://linkedin.com/in/anchal-developer)
- Portfolio: https://anchals7.github.io/anchalsr.github.io/

---

## 🙏 Acknowledgments

- **Climatiq** for emissions data API
- **Google Gemini** for natural language processing
- **Supabase** for database infrastructure
- **Prophet** (Facebook) for time-series forecasting
- **Next.js & FastAPI** communities for excellent documentation

---

<div align="center">

**Built with ❤️ for a sustainable future**

[⭐ Star this repo](https://github.com/yourusername/EcoTrackAI) | [📧 Contact](mailto:your.email@example.com) | [🐛 Report Bug](https://github.com/yourusername/EcoTrackAI/issues)

</div>
