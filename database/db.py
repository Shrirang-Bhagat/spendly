import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


def seed_db():
    db = get_db()
    row = db.execute("SELECT COUNT(*) FROM users").fetchone()
    if row[0] > 0:
        db.close()
        return

    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 12.50,  "Food",          "2026-04-01", "Lunch at cafe"),
        (user_id, 45.00,  "Transport",     "2026-04-03", "Monthly bus pass"),
        (user_id, 120.00, "Bills",         "2026-04-05", "Electricity bill"),
        (user_id, 30.00,  "Health",        "2026-04-08", "Pharmacy"),
        (user_id, 25.00,  "Entertainment", "2026-04-10", "Movie tickets"),
        (user_id, 85.00,  "Shopping",      "2026-04-13", "Clothing"),
        (user_id, 15.75,  "Other",         "2026-04-15", "Miscellaneous"),
        (user_id, 9.99,   "Food",          "2026-04-18", "Coffee and snacks"),
    ]
    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    db.commit()
    db.close()


def create_user(name: str, email: str, password: str) -> int:
    password_hash = generate_password_hash(password)
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    user_id = cursor.lastrowid
    db.commit()
    db.close()
    return user_id
