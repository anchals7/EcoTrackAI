# Backend Environment Variables Setup

## Quick Start

1. **Copy the example file:**
   ```bash
   cd backend
   cp env.example .env
   ```

2. **Edit `.env` and add your API keys:**
   - Open `.env` in a text editor
   - Replace placeholder values with your actual API keys

## Required Variables

### 🔑 GEMINI_API_KEY (Required)
**Purpose:** Natural language parsing and recommendation enhancement

**How to get it:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in `.env` as: `GEMINI_API_KEY=your_key_here`

**Example:**
```
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 🔑 CLIMATIQ_API_KEY (Required)
**Purpose:** Calculate CO₂ emissions for activities

**How to get it:**
1. Go to [Climatiq.io](https://www.climatiq.io/)
2. Sign up for a free account
3. Navigate to API section in dashboard
4. Copy your API key
5. Paste it in `.env` as: `CLIMATIQ_API_KEY=your_key_here`

**Example:**
```
CLIMATIQ_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Optional Variables

### Supabase (Optional for MVP)
Currently, the MVP uses in-memory storage. If you want to use Supabase:

1. Create a project at [Supabase](https://supabase.com/)
2. Get your project URL and service role key
3. Add to `.env`:
   ```
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your_service_role_key
   DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
   ```

### JWT Secret (Optional for MVP)
Only needed if you implement authentication:

```bash
# Generate a secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then add to `.env`:
```
JWT_SECRET=your_generated_secret_here
JWT_ALGORITHM=HS256
```

## Complete .env Example

```env
# Required API Keys
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLIMATIQ_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional - Supabase (for future database integration)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_service_role_key
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

# Optional - JWT (for future authentication)
JWT_SECRET=your_random_secret_key_here
JWT_ALGORITHM=HS256

# Environment
ENVIRONMENT=development
```

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` to git (it's in `.gitignore`)
- Never share your API keys publicly
- Use different keys for development and production
- Rotate keys if they're accidentally exposed

## Testing Your Setup

After setting up `.env`, test that the backend can read it:

```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GEMINI:', 'SET' if os.getenv('GEMINI_API_KEY') else 'MISSING'); print('CLIMATIQ:', 'SET' if os.getenv('CLIMATIQ_API_KEY') else 'MISSING')"
```

You should see:
```
GEMINI: SET
CLIMATIQ: SET
```

## Troubleshooting

### "GEMINI_API_KEY not configured"
- Check that `.env` file exists in the `backend/` directory
- Verify the key name is exactly `GEMINI_API_KEY` (case-sensitive)
- Make sure there are no extra spaces or quotes around the value

### "CLIMATIQ_API_KEY not configured"
- Same checks as above
- Verify your Climatiq API key is active in their dashboard

### Environment variables not loading
- Make sure `python-dotenv` is installed: `pip install python-dotenv`
- Verify you're running the backend from the `backend/` directory
- Check that `.env` is in the same directory as `main.py`

