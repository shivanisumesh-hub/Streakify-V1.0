# Streakify V1.0 MVP Backend

Streakify is a backend API for tracking habits, daily progress, streaks, and productivity insights. It is designed as an MVP for a habit-building product where users can register, create habits, log completions, monitor streak momentum, and review performance analytics.

The backend is built with FastAPI, SQLAlchemy, and PostgreSQL, with a clean layered structure that makes the codebase easy to test and extend.

## Features

- User registration, profile lookup, and account deletion
- Habit creation, listing, and deletion
- Daily habit logging with duplicate prevention
- Historical habit logging by date
- Future-date log validation
- Calendar-aware current and longest streak calculation
- Productivity dashboard with habit streak summaries
- Layered architecture with routers, services, CRUD, schemas, and models

## Business Rules

- A user can create multiple habits.
- Each habit belongs to one user.
- A habit log belongs to one habit.
- A habit can be logged only once per calendar date.
- Future dates cannot be logged.
- Missing calendar days break the current streak.
- The longest streak is preserved even after a streak is broken.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest

## Project Structure

```text
app/
  crud/          Database access functions
  models/        SQLAlchemy database models
  routers/       FastAPI route definitions
  schemas/       Pydantic request and response models
  services/      Business logic
  config.py      Database configuration
  main.py        FastAPI application entry point
tests/
  test_main.py   API test coverage
schema.sql       PostgreSQL schema initialization script
```

## Database Configuration

This project is configured to use the local PostgreSQL database:

```text
streakifyv1_db
```

The connection string is defined in `app/config.py`:

```python
postgresql://apple@localhost:5432/streakifyv1_db
```

Create the database:

```bash
createdb streakifyv1_db
```

Initialize the schema:

```bash
psql -d streakifyv1_db -f schema.sql
```

## Database Tables

The PostgreSQL schema contains three main tables:

| Table | Purpose |
| --- | --- |
| `users` | Stores user profile details |
| `habits` | Stores user-created habits and target frequency |
| `habit_logs` | Stores daily completion status for each habit |

Important constraints and indexes:

- `users.email` is unique.
- `habits.user_id` references `users.id`.
- `habit_logs.habit_id` references `habits.id`.
- `(habit_id, log_date)` is unique to prevent duplicate logs.
- Indexes are included for email lookup, user habits, and habit log date queries.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary "pydantic[email]" pytest
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
venv/bin/python -m pytest -q
```

The test suite uses an in-memory SQLite database so tests can run without modifying the local PostgreSQL database.

## API Endpoints

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/users` | Register a user |
| GET | `/users/{id}` | View user profile |
| DELETE | `/users/{id}` | Delete user and related data |

### Habits

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/habits` | Create a habit |
| GET | `/users/{userId}/habits` | View all habits for a user |
| DELETE | `/habits/{id}` | Delete a habit |

### Habit Logs

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/habits/{habitId}/logs` | Log progress for today or a specific date |
| PUT | `/habits/{habitId}/logs/{date}` | Edit an existing log |
| GET | `/habits/{habitId}/logs` | View habit logs |

### Streaks

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/habits/{habitId}/streak` | Get current and longest streak |

### Dashboard

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/users/{userId}/dashboard` | Get productivity dashboard |

## Sample Requests

### Create User

```http
POST /users
Content-Type: application/json
```

```json
{
  "name": "Alice Smith",
  "email": "alice@example.com"
}
```

Sample response:

```json
{
  "id": 1,
  "name": "Alice Smith",
  "email": "alice@example.com",
  "created_at": "2026-06-22T10:30:00+00:00"
}
```

### Create Habit

```http
POST /habits
Content-Type: application/json
```

```json
{
  "name": "Morning Workout",
  "target_days_per_week": 5,
  "user_id": 1
}
```

### Log Habit For A Specific Date

```http
POST /habits/1/logs
Content-Type: application/json
```

```json
{
  "log_date": "2026-06-20",
  "completed": true
}
```

If `log_date` is omitted, the API logs the habit for the current date.

### Edit Habit Log

```http
PUT /habits/1/logs/2026-06-20
Content-Type: application/json
```

```json
{
  "completed": false
}
```

### Get Streak

```http
GET /habits/1/streak
```

Sample response:

```json
{
  "habit_id": 1,
  "current_streak": 2,
  "max_streak": 5
}
```

### Get Dashboard

```http
GET /users/1/dashboard
```

Sample response:

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

## Validation And Error Cases

- Duplicate user email returns `400`.
- Invalid email returns `422`.
- Non-existing user or habit returns `404`.
- Duplicate habit log for the same date returns `400`.
- Future date logging returns `400`.
- Invalid date format for log update returns `400`.

## Testing

The automated tests cover:

- User lifecycle
- Habit lifecycle
- Duplicate user validation
- Duplicate habit log validation
- Future-date log validation
- Multi-day habit logging
- Calendar gap streak reset
- Dashboard response data

## Postman Testing Checklist

Use the API docs or a Postman collection to test:

- Create user
- Create habit
- Log multiple days
- Break a streak by skipping a date
- Fetch streak
- Fetch dashboard
- Duplicate log negative case
- Future date negative case
- Non-existing user negative case
- Invalid email negative case
