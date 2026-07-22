import sqlite3

connection = sqlite3.connect("data/memory.db")
cursor = connection.cursor()

cursor.execute("SELECT filename, timestamp, ocr_text FROM screenshots")
rows = cursor.fetchall()

print(f"Total rows: {len(rows)}")
print("---")

for row in rows[:5]:
    filename, timestamp, ocr_text = row
    print(f"File: {filename}")
    print(f"Time: {timestamp}")
    print(f"Text: {ocr_text[:100]}...")
    print("---")

connection.close()