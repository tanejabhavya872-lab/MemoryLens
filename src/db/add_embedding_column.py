import sqlite3

connection = sqlite3.connect("data/memory.db")
cursor = connection.cursor()

cursor.execute("ALTER TABLE screenshots ADD COLUMN embedding TEXT")

connection.commit()
connection.close()

print("Column added successfully.")
