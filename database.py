import json
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "data" / "gramsathi.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialise_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entrepreneur_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                state TEXT,
                district TEXT,
                village TEXT,
                education TEXT,
                budget INTEGER,
                experience TEXT,
                skills TEXT,
                interests TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS market_surveys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entrepreneur_name TEXT NOT NULL,
                business_name TEXT NOT NULL,
                potential_customers INTEGER,
                competitors INTEGER,
                average_spend INTEGER,
                demand TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_profile(profile: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO entrepreneur_profiles
            (name, age, state, district, village, education, budget, experience, skills, interests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile["name"], profile["age"], profile["state"], profile["district"],
                profile["village"], profile["education"], profile["budget"], profile["experience"],
                json.dumps(profile["skills"], ensure_ascii=False),
                json.dumps(profile["interests"], ensure_ascii=False),
            ),
        )


def save_market_survey(entrepreneur_name: str, business_name: str, survey: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO market_surveys
            (entrepreneur_name, business_name, potential_customers, competitors, average_spend, demand, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entrepreneur_name, business_name, survey["potential_customers"],
                survey["competitors"], survey["average_spend"], survey["demand"], survey["notes"],
            ),
        )


def get_dashboard_stats() -> dict:
    with get_connection() as conn:
        profile_count = conn.execute("SELECT COUNT(*) FROM entrepreneur_profiles").fetchone()[0]
        survey_count = conn.execute("SELECT COUNT(*) FROM market_surveys").fetchone()[0]
    return {"profiles": profile_count, "surveys": survey_count}
