import sqlite3

# Connect to SQLite database (creates obd_data.db if not exists)
conn = sqlite3.connect("obd_data.db")
cursor = conn.cursor()

# Create OBD codes table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS obd_codes (
        code TEXT PRIMARY KEY,
        description TEXT
    )
""")

# Insert mock OBD data
mock_data = [
    ("P0420", "Catalyst System Efficiency Below Threshold (Bank 1)"),
    ("P0300", "Random/Multiple Cylinder Misfire Detected"),
    ("P0171", "System Too Lean (Bank 1)")
]
cursor.executemany("INSERT OR IGNORE INTO obd_codes VALUES (?, ?)", mock_data)

# Create query history table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_query TEXT,
        response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()
print("Database initialized with mock OBD data.")