# Streakify - Habit Tracking API

## Overview

Streakify is a backend habit tracking application designed to help users build consistent habits and improve productivity by maintaining daily streaks. The system allows users to create habits, log daily progress, track current and longest streaks, and view productivity insights through a dashboard API.

The application provides a structured backend using FastAPI, SQLAlchemy, and PostgreSQL. It follows a layered architecture to keep routing, business logic, validation, and database operations cleanly separated.

---

## Features

- User Management
  - Create, fetch, and delete users
  - Unique email validation
  - Invalid email validation

- Habit Management
  - Create and delete habits
  - Set target days per week
  - View all habits for a user

- Habit Tracking
  - Log daily habit completion
  - Log progress for a specific date
  - Edit existing habit logs
  - Prevent duplicate entries for the same habit and date
  - Prevent future date entries

- Streak Calculation
  - Tracks current streak
  - Calculates longest streak
  - Breaks streaks when calendar days are missed

- Dashboard
  - Shows total habits
  - Shows completed habits for today
  - Displays current and longest streak summaries
  - Calculates consistency score

- Validation & Error Handling
  - Field validation for request bodies
  - Custom exception handling for:
    - Duplicate email
    - Duplicate habit logs
    - Resource not found
    - Invalid dates
    - Future date logging

- RESTful API Design
  - Clean and structured endpoints
  - Proper HTTP methods: GET, POST, PUT, DELETE
  - JSON request and response bodies

- Layered Architecture
  - Router -> Service -> CRUD separation
  - SQLAlchemy models for database mapping
  - Pydantic schemas for validation and serialization

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Pytest
- Postman

---

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/shivanisumesh-hub/Streakify-V1.0.git
cd Streakify-V1.0
```

### 2. Create PostgreSQL Database

Create a database named:

```text
streakifyv1_db
```

Example command:

```bash
createdb streakifyv1_db
```

### 3. Initialize Database Schema

Run the schema file:

```bash
psql -d streakifyv1_db -f schema.sql
```

### 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary "pydantic[email]" pytest
```

### 6. Configure Database

The database connection is configured in `app/config.py`:

```python
postgresql://apple@localhost:5432/streakifyv1_db
```

Update this connection string if your PostgreSQL username, password, host, port, or database name is different.

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

Server runs on:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Database Schema

### users

| Column | Type |
| --- | --- |
| id | SERIAL PRIMARY KEY |
| name | VARCHAR(100) NOT NULL |
| email | VARCHAR(255) UNIQUE NOT NULL |
| created_at | TIMESTAMP WITH TIME ZONE |

---

### habits

| Column | Type |
| --- | --- |
| id | SERIAL PRIMARY KEY |
| name | VARCHAR(150) NOT NULL |
| target_days_per_week | INT CHECK BETWEEN 1 AND 7 |
| user_id | INT FOREIGN KEY -> users.id |
| created_at | TIMESTAMP WITH TIME ZONE |

---

### habit_logs

| Column | Type |
| --- | --- |
| id | SERIAL PRIMARY KEY |
| habit_id | INT FOREIGN KEY -> habits.id |
| log_date | DATE |
| completed | BOOLEAN |

Constraints and indexes:

- Unique constraint on `(habit_id, log_date)`
- Index on `users.email`
- Index on `habits.user_id`
- Index on `(habit_id, log_date)`
- Cascade delete from users to habits
- Cascade delete from habits to habit logs

---

## Project Structure

```text
streakify/
|-- app/
|   |-- crud/
|   |   |-- habit.py
|   |   |-- habit_log.py
|   |   |-- streak.py
|   |   |-- user.py
|   |
|   |-- models/
|   |   |-- habit.py
|   |   |-- habit_log.py
|   |   |-- user.py
|   |
|   |-- routers/
|   |   |-- dashboards.py
|   |   |-- habit_logs.py
|   |   |-- habits.py
|   |   |-- streaks.py
|   |   |-- users.py
|   |
|   |-- schemas/
|   |   |-- habit.py
|   |   |-- habit_log.py
|   |   |-- user.py
|   |
|   |-- services/
|   |   |-- dashboard_service.py
|   |   |-- habit_log_service.py
|   |   |-- habit_service.py
|   |   |-- streak_service.py
|   |   |-- user_service.py
|   |
|   |-- config.py
|   |-- main.py
|
|-- tests/
|   |-- test_main.py
|
|-- schema.sql
|-- README.md
```

---

## API Endpoints

### User APIs

- POST `/users`
- GET `/users/{id}`
- DELETE `/users/{id}`

### Habit APIs

- POST `/habits`
- GET `/users/{userId}/habits`
- DELETE `/habits/{id}`

### Habit Log APIs

- POST `/habits/{habitId}/logs`
- PUT `/habits/{habitId}/logs/{date}`
- GET `/habits/{habitId}/logs`

### Streak API

- GET `/habits/{habitId}/streak`

### Dashboard API

- GET `/users/{userId}/dashboard`

---

## Sample API

### Create User

POST `/users`

Request:

```json
{
  "name": "Alice Smith",
  "email": "alice@example.com"
}
```

Response:

```json
{
  "id": 1,
  "name": "Alice Smith",
  "email": "alice@example.com",
  "created_at": "2026-06-22T10:30:00+00:00"
}
```

### Create Habit

POST `/habits`

Request:

```json
{
  "name": "Morning Workout",
  "target_days_per_week": 5,
  "user_id": 1
}
```

Response:

```json
{
  "id": 1,
  "name": "Morning Workout",
  "target_days_per_week": 5,
  "user_id": 1,
  "created_at": "2026-06-22T10:31:00+00:00"
}
```

### Log Habit

POST `/habits/1/logs`

Request:

```json
{
  "log_date": "2026-06-20",
  "completed": true
}
```

Response:

```json
{
  "id": 1,
  "habit_id": 1,
  "log_date": "2026-06-20",
  "completed": true
}
```

If `log_date` is omitted, the API logs the habit for the current date.

### Edit Habit Log

PUT `/habits/1/logs/2026-06-20`

Request:

```json
{
  "completed": false
}
```

Response:

```json
{
  "id": 1,
  "habit_id": 1,
  "log_date": "2026-06-20",
  "completed": false
}
```

### Get Streak

GET `/habits/1/streak`

Response:

```json
{
  "habit_id": 1,
  "current_streak": 2,
  "max_streak": 5
}
```

### Get Dashboard

GET `/users/1/dashboard`

Response:

```json
{
  "totalHabits": 2,
  "activeHabits": 2,
  "completedToday": 1,
  "currentStreaks": [
    {
      "habitName": "Morning Workout",
      "currentStreak": 2,
      "longestStreak": 5
    }
  ],
  "consistencyScore": 80.0
}
```

### Error Response Examples

Duplicate email:

```json
{
  "detail": "Email already registered"
}
```

Duplicate habit log:

```json
{
  "detail": "Habit already logged for this date"
}
```

Future date log:

```json
{
  "detail": "Cannot log habits for a future date"
}
```

---

## Testing

Run tests:

```bash
venv/bin/python -m pytest -q
```

The tests use an in-memory SQLite database so they do not modify the local PostgreSQL database.

Test coverage includes:

- User lifecycle
- Habit lifecycle
- Duplicate user validation
- Duplicate habit log validation
- Future date validation
- Multi-day habit logging
- Calendar gap streak reset
- Dashboard response data

---

## Postman Testing Checklist

- Create user
- Create habit
- Log multiple days
- Break a streak by skipping a date
- Fetch streak
- Fetch dashboard
- Test duplicate log
- Test future date log
- Test non-existing user
- Test invalid email
