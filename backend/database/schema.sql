-- EcoTrack AI Database Schema for Supabase
-- Run this in your Supabase SQL Editor

-- Activities table
CREATE TABLE IF NOT EXISTS activities (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL DEFAULT 'user_001',
    activity_category TEXT NOT NULL,
    activity_subtype TEXT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    unit TEXT NOT NULL,
    co2e_kg DECIMAL(10, 4) NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_activities_user_id ON activities(user_id);
CREATE INDEX IF NOT EXISTS idx_activities_date ON activities(date);
CREATE INDEX IF NOT EXISTS idx_activities_category ON activities(activity_category);

-- Enable Row Level Security (optional, for multi-user support later)
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;

-- Policy to allow all operations for now (for MVP)
CREATE POLICY "Allow all operations for MVP" ON activities
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Users table (for future authentication)
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create index for users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

