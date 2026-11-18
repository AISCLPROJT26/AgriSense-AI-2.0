import sqlite3
from pathlib import Path

def init_db(db_path=None):
    if db_path is None:
        db_path = Path(__file__).resolve().parent / "agrisense.db"

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Offline Mandi Prices Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mandi_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT NOT NULL,
            mandi TEXT NOT NULL,
            min_price INTEGER NOT NULL,
            max_price INTEGER NOT NULL,
            modal_price INTEGER NOT NULL,
            trend TEXT DEFAULT 'up',
            change_pct TEXT DEFAULT '+1.5%'
        )
    """)

    # Seed default regional Mandi rates if empty
    cursor.execute("SELECT COUNT(*) FROM mandi_prices")
    if cursor.fetchone()[0] == 0:
        default_rates = [
            ("Wheat (Gehun)", "Meerut Mandi, UP", 2380, 2520, 2460, "up", "+1.8%"),
            ("Basmati Rice (Dhan)", "Muzaffarnagar, UP", 3650, 4100, 3890, "up", "+2.4%"),
            ("Sugarcane (Ganna)", "Baghpat Zone, UP", 360, 375, 370, "stable", "0.0%"),
            ("Potato (Aloo)", "Hapur Mandi, UP", 1150, 1420, 1290, "down", "-1.2%"),
            ("Mustard (Sarson)", "Bulandshahr, UP", 5450, 5780, 5620, "up", "+3.1%"),
            ("Tomato (Tamatar)", "Meerut Mandi, UP", 1600, 2100, 1850, "up", "+4.5%")
        ]
        cursor.executemany("""
            INSERT INTO mandi_prices (crop, mandi, min_price, max_price, modal_price, trend, change_pct)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, default_rates)

    conn.commit()
    conn.close()