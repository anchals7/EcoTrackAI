# Database Setup Guide (Supabase)

## Why Use Supabase?

- **Persistent Storage**: Data survives server restarts
- **Low Memory Usage**: No in-memory storage burden
- **Scalable**: Can handle more data as you grow
- **Free Tier**: Generous free tier for MVP/demo

## Quick Setup

### 1. Create Supabase Project

1. Go to [Supabase](https://supabase.com/)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: EcoTrackAI (or your choice)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to you
5. Wait for project to be created (~2 minutes)

### 2. Get Your Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **Service Role Key** (secret) → `SUPABASE_KEY`

### 3. Create Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy and paste the contents of `database/schema.sql`
4. Click **Run** (or press Ctrl+Enter)
5. You should see "Success. No rows returned"

### 4. Configure Backend

1. Open `backend/.env` file
2. Add your Supabase credentials:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_service_role_key_here
```

3. Save the file

### 5. Test Connection

Start your backend:

```bash
cd backend
uvicorn main:app --reload
```

You should see:
```
✅ Connected to Supabase
```

If you see:
```
⚠️  Supabase not configured. Using in-memory storage.
```

Check that:
- `.env` file exists in `backend/` directory
- Credentials are correct (no extra spaces)
- You're using the **Service Role Key** (not anon key)

## Database Schema

The schema creates one main table:

### `activities` table
- `id` - UUID primary key
- `user_id` - Text (defaults to 'user_001' for MVP)
- `activity_category` - Text (transportation, food, energy, etc.)
- `activity_subtype` - Text (car, beef, electricity, etc.)
- `amount` - Decimal
- `unit` - Text (miles, kg, kWh, etc.)
- `co2e_kg` - Decimal (calculated emissions)
- `date` - Timestamp
- `created_at` - Timestamp

## Fallback Behavior

The code is designed to gracefully fall back to in-memory storage if:
- Supabase is not configured
- Database connection fails
- Tables don't exist

This means:
- ✅ You can test without Supabase (uses in-memory)
- ✅ If Supabase has issues, app still works (with in-memory)
- ✅ Easy to switch between storage methods

## Verifying It Works

1. **Log an activity** via the frontend
2. **Check Supabase**:
   - Go to **Table Editor** → **activities**
   - You should see your logged activity
3. **Restart backend**:
   - Data should still be there (not lost like in-memory)

## Troubleshooting

### "Table does not exist"
- Run the SQL schema in Supabase SQL Editor
- Check table name is exactly `activities` (lowercase)

### "Permission denied"
- Make sure you're using **Service Role Key** (not anon key)
- Check Row Level Security policies in Supabase

### "Connection timeout"
- Check your internet connection
- Verify SUPABASE_URL is correct
- Try accessing Supabase dashboard to confirm project is active

### Data not persisting
- Check Supabase dashboard → Table Editor
- Verify data is actually being saved
- Check backend logs for errors

## Next Steps

Once database is working:
- ✅ Data persists across restarts
- ✅ Can handle more data without memory issues
- ✅ Ready for multi-user support (add authentication)
- ✅ Can add more tables (users, goals, etc.)

## Security Notes

⚠️ **Important:**
- Service Role Key has full access - keep it secret!
- Never commit `.env` to git
- For production, use environment-specific keys
- Consider Row Level Security policies for multi-user

