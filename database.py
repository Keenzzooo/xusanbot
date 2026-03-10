import aiosqlite
import json
from typing import Optional
from config import DATABASE_PATH


async def init_db():
    """Initialize the database and create tables if they don't exist."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id     INTEGER UNIQUE NOT NULL,
                username        TEXT,
                first_name      TEXT,
                name_history    TEXT DEFAULT '[]',
                messages_count  INTEGER DEFAULT 0,
                groups_count    INTEGER DEFAULT 0,
                channels_count  INTEGER DEFAULT 0,
                media_percent   REAL DEFAULT 0.0,
                reply_percent   REAL DEFAULT 0.0,
                favorite_chat   TEXT DEFAULT 'N/A'
            )
        """)
        await db.commit()
    await seed_sample_data()


async def seed_sample_data():
    """Insert sample users into the database if it's empty."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        count = (await cursor.fetchone())[0]

        if count == 0:
            sample_users = [
                (
                    123456789, "john_doe", "John",
                    json.dumps(["Johnny", "John D.", "John"]),
                    4821, 12, 5, 34.5, 22.1, "Tech Talk Group"
                ),
                (
                    987654321, "jane_smith", "Jane",
                    json.dumps(["Janie", "Jane S."]),
                    2390, 8, 3, 61.2, 45.0, "Design Hub"
                ),
                (
                    111222333, "alex_dev", "Alex",
                    json.dumps(["Alex Dev", "Alexander"]),
                    9105, 20, 10, 18.7, 30.5, "Dev Corner"
                ),
                (
                    444555666, "maria_k", "Maria",
                    json.dumps(["Mari", "Maria K"]),
                    1560, 4, 2, 75.0, 10.3, "Photo Lovers"
                ),
                (
                    777888999, "crypto_bob", "Bob",
                    json.dumps(["Bob", "Robert", "crypto_rob"]),
                    7342, 15, 8, 22.4, 55.8, "Crypto Signals"
                ),
            ]

            await db.executemany("""
                INSERT OR IGNORE INTO users
                    (telegram_id, username, first_name, name_history, messages_count,
                     groups_count, channels_count, media_percent, reply_percent, favorite_chat)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_users)
            await db.commit()


async def get_user_by_id(telegram_id: int) -> Optional[dict]:
    """Fetch a user by their Telegram ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
    return None


async def get_user_by_username(username: str) -> Optional[dict]:
    """Fetch a user by their username (case-insensitive, with or without @)."""
    username = username.lstrip("@").lower()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE LOWER(username) = ?", (username,)
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
    return None


async def get_all_users() -> list[dict]:
    """Return all users from the database."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users ORDER BY messages_count DESC"
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_top_users(limit: int = 5) -> list[dict]:
    """Return top users sorted by message count."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users ORDER BY messages_count DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]
