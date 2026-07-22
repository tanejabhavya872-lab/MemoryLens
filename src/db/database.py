import sqlite3

connection = sqlite3.connect("data/memory.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS screenshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        ocr_text TEXT
    )
""")

connection.commit()
connection.close()

print("Database and table created successfully.")