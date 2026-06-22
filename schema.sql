-- ==============================================================================
-- Streakify Database Initialization DDL Script (PostgreSQL)
-- ==============================================================================

-- 1. Drop existing tables if they exist to prevent schema conflicts on recreation
DROP TABLE IF EXISTS habit_logs CASCADE;
DROP TABLE IF EXISTS habits CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. Create Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Habits Table (Belongs to a specific user)
CREATE TABLE habits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    target_days_per_week INT NOT NULL CHECK (target_days_per_week BETWEEN 1 AND 7),
    user_id INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Create Habit Logs Table (Tracks daily completions)
CREATE TABLE habit_logs (
    id SERIAL PRIMARY KEY,
    habit_id INT NOT NULL,
    log_date DATE NOT NULL DEFAULT CURRENT_DATE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_habit FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
    CONSTRAINT unique_habit_per_day UNIQUE (habit_id, log_date)
);

-- 5. Add Performance Optimizing Indexes for fast API lookup operations
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_habits_user ON habits(user_id);
CREATE INDEX idx_habit_logs_date ON habit_logs(habit_id, log_date);
