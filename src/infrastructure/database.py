import sqlite3
from sqlite3 import Connection
from contextlib import contextmanager
import os

DATABASE_PATH = "habit_builder.db"

def init_db():
    with get_db() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                goals TEXT
            );

            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                frequency TEXT NOT NULL,
                streak INTEGER DEFAULT 0,
                created_at TIMESTAMP NOT NULL,
                reminder_time TIMESTAMP,
                last_completed TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );

            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                creator_id INTEGER NOT NULL,
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                FOREIGN KEY (creator_id) REFERENCES users (id)
            );

            CREATE TABLE IF NOT EXISTS challenge_participants (
                challenge_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                joined_at TIMESTAMP NOT NULL,
                PRIMARY KEY (challenge_id, user_id),
                FOREIGN KEY (challenge_id) REFERENCES challenges (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        ''')

@contextmanager
def get_db() -> Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()