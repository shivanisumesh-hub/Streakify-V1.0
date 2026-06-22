import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.config import Base, engine
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_database_per_test():
    # Force drop and re-creation directly on the shared StaticPool memory engine space
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ==============================================================================
# 1. USER ENDPOINT APIS
# ==============================================================================

def test_user_lifecycle_api():
    """Validates User Registration, Profile Retrieval, and Cascade Removal."""
    response = client.post("/users", json={"name": "Alice Smith", "email": "alice@litmus7.com"})
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["name"] == "Alice Smith"
    user_id = user_data["id"]

    dup_res = client.post("/users", json={"name": "Alice Clone", "email": "alice@litmus7.com"})
    assert dup_res.status_code == 400
    assert dup_res.json()["detail"] == "Email already registered"

    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["email"] == "alice@litmus7.com"

    get_missing_res = client.get("/users/99999")
    assert get_missing_res.status_code == 404

    del_res = client.delete(f"/users/{user_id}")
    assert del_res.status_code == 200
    
    get_gone_res = client.get(f"/users/{user_id}")
    assert get_gone_res.status_code == 404

# ==============================================================================
# 2. HABIT ENDPOINT APIS
# ==============================================================================

def test_habit_lifecycle_api():
    """Validates Habit creation constraints and list retrieval mechanics."""
    u_res = client.post("/users", json={"name": "Bob Dylan", "email": "bob@test.com"})
    user_id = u_res.json()["id"]

    h_res = client.post("/habits", json={"name": "Drink Water", "target_days_per_week": 7, "user_id": user_id})
    assert h_res.status_code == 201
    habit_id = h_res.json()["id"]

    list_res = client.get(f"/users/{user_id}/habits")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    del_h_res = client.delete(f"/habits/{habit_id}")
    assert del_h_res.status_code == 200

# ==============================================================================
# 3. HABIT LOG ENDPOINT APIS
# ==============================================================================

def test_habit_logging_validation_api():
    """Verifies daily logs register properly, intercepting duplicates and future logs."""
    u_res = client.post("/users", json={"name": "Charlie", "email": "charlie@test.com"})
    user_id = u_res.json()["id"]
    h_res = client.post("/habits", json={"name": "Yoga", "target_days_per_week": 3, "user_id": user_id})
    habit_id = h_res.json()["id"]

    log_res = client.post(f"/habits/{habit_id}/logs", json={"completed": True})
    assert log_res.status_code == 201

    dup_res = client.post(f"/habits/{habit_id}/logs", json={"completed": True})
    assert dup_res.status_code == 400
    assert dup_res.json()["detail"] == "Habit already logged for today"

    tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    future_res = client.put(f"/habits/{habit_id}/logs/{tomorrow_str}", json={"completed": True})
    assert future_res.status_code == 400
    assert future_res.json()["detail"] == "Cannot log habits for a future date"

# ==============================================================================
# 4. STREAK ENGINE & DASHBOARD INSIGHT APIS
# ==============================================================================

def test_streak_and_dashboard_calculations_api():
    """Traces calculations for active streak profiles and productivity summaries."""
    u_res = client.post("/users", json={"name": "Dani", "email": "dani@test.com"})
    user_id = u_res.json()["id"]
    h_res = client.post("/habits", json={"name": "Running", "target_days_per_week": 5, "user_id": user_id})
    habit_id = h_res.json()["id"]

    client.post(f"/habits/{habit_id}/logs", json={"completed": True})

    streak_res = client.get(f"/habits/{habit_id}/streak")
    assert streak_res.status_code == 200
    assert streak_res.json()["current_streak"] == 1

    dash_res = client.get(f"/users/{user_id}/dashboard")
    assert dash_res.status_code == 200
    dashboard = dash_res.json()
    assert dashboard["totalHabits"] == 1
    assert dashboard["activeHabits"] == 1
    assert dashboard["completedToday"] == 1
    assert dashboard["currentStreaks"][0]["habitName"] == "Running"
    assert dashboard["currentStreaks"][0]["currentStreak"] == 1
    assert dashboard["currentStreaks"][0]["longestStreak"] == 1


def test_calendar_gaps_break_streaks_api():
    """Validates multi-day logging and streak reset when a calendar day is missed."""
    u_res = client.post("/users", json={"name": "Eli", "email": "eli@test.com"})
    user_id = u_res.json()["id"]
    h_res = client.post("/habits", json={"name": "Read", "target_days_per_week": 5, "user_id": user_id})
    habit_id = h_res.json()["id"]

    four_days_ago = (date.today() - timedelta(days=4)).strftime("%Y-%m-%d")
    three_days_ago = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")

    assert client.post(f"/habits/{habit_id}/logs", json={"log_date": four_days_ago, "completed": True}).status_code == 201
    assert client.post(f"/habits/{habit_id}/logs", json={"log_date": three_days_ago, "completed": True}).status_code == 201
    assert client.post(f"/habits/{habit_id}/logs", json={"log_date": yesterday, "completed": True}).status_code == 201
    assert client.post(f"/habits/{habit_id}/logs", json={"log_date": today, "completed": True}).status_code == 201

    streak_res = client.get(f"/habits/{habit_id}/streak")
    assert streak_res.status_code == 200
    streak = streak_res.json()
    assert streak["current_streak"] == 2
    assert streak["max_streak"] == 2

    dup_res = client.post(f"/habits/{habit_id}/logs", json={"log_date": yesterday, "completed": True})
    assert dup_res.status_code == 400
    assert dup_res.json()["detail"] == "Habit already logged for this date"
