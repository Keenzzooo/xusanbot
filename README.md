# 🤖 Database Analyzer Bot

A Telegram bot built with **Python + aiogram 3** that looks up users in a local
SQLite database and returns formatted statistics with inline keyboard navigation.

---

## ✨ Features

| Feature | Detail |
|---|---|
| Search by ID or username | Send `123456789` or `@john_doe` |
| Full profile view | ID, username, name |
| Statistics | Messages, groups, channels, media %, reply % |
| Name history | All past display names |
| Analysis | Activity level & communication style |
| Share card | Forwardable profile summary |
| Inline keyboard | Profile / Groups / Messages / Analysis / Share |
| /start & /menu commands | Entry points |

---

## 🚀 Quick Start (local)

```bash
# 1. Clone / download the project
cd database_analyzer_bot

# 2. Create & activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set your BOT_TOKEN

# 5. Run the bot
python bot.py
```

The SQLite database (`users.db`) is created automatically on first run and
seeded with 5 sample users.

---

## 🗄️ Database Schema

```sql
CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id     INTEGER UNIQUE NOT NULL,
    username        TEXT,
    first_name      TEXT,
    name_history    TEXT DEFAULT '[]',   -- JSON array of past names
    messages_count  INTEGER DEFAULT 0,
    groups_count    INTEGER DEFAULT 0,
    channels_count  INTEGER DEFAULT 0,
    media_percent   REAL DEFAULT 0.0,
    reply_percent   REAL DEFAULT 0.0,
    favorite_chat   TEXT DEFAULT 'N/A'
);
```

### Adding your own users

```python
import aiosqlite, json, asyncio

async def add_user():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
            INSERT INTO users
                (telegram_id, username, first_name, name_history,
                 messages_count, groups_count, channels_count,
                 media_percent, reply_percent, favorite_chat)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            100000001, "new_user", "Alice",
            json.dumps(["Alice", "ali_ce"]),
            3000, 7, 4, 45.0, 30.0, "Python Devs"
        ))
        await db.commit()

asyncio.run(add_user())
```

---

## ☁️ Deploy to Railway (free tier)

1. Push this folder to a **GitHub repo**.
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
3. Select your repo.
4. In the **Variables** tab add:
   - `BOT_TOKEN` = your token from [@BotFather](https://t.me/BotFather)
5. Railway uses the `Procfile` (`worker: python bot.py`) automatically.
6. Click **Deploy**. ✅

> **Persistence note:** Railway's free tier has an ephemeral filesystem.
> The SQLite file is recreated (with seed data) on every restart.
> For persistent storage, use Railway's **PostgreSQL** plugin or mount a volume.

---

## ☁️ Deploy to Render (free tier)

1. Push this folder to a **GitHub repo**.
2. Go to [render.com](https://render.com) → **New** → **Background Worker**.
3. Connect your repo.
4. Render will detect `render.yaml` automatically.
5. Add environment variable `BOT_TOKEN` in the dashboard.
6. Click **Deploy**. ✅

---

## 📁 Project Structure

```
database_analyzer_bot/
├── bot.py           # Entry point – starts polling
├── config.py        # Reads .env / environment variables
├── database.py      # SQLite helpers (init, seed, queries)
├── handlers.py      # All aiogram handlers (commands + callbacks)
├── keyboards.py     # InlineKeyboardMarkup builders
├── formatters.py    # Message text formatters
├── requirements.txt
├── Procfile         # Railway / Heroku worker
├── render.yaml      # Render deployment config
└── .env.example     # Template for environment variables
```

---

## 🔍 Sample Users (seeded automatically)

| ID | Username | Name | Messages |
|---|---|---|---|
| 123456789 | @john_doe | John | 4 821 |
| 987654321 | @jane_smith | Jane | 2 390 |
| 111222333 | @alex_dev | Alex | 9 105 |
| 444555666 | @maria_k | Maria | 1 560 |
| 777888999 | @crypto_bob | Bob | 7 342 |

---

## 📜 License

MIT — free to use and modify.
