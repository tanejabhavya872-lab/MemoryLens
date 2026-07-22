import easyocr
import os
import sqlite3

reader = easyocr.Reader(['en'])

connection = sqlite3.connect("data/memory.db")
cursor = connection.cursor()

screenshots_folder = "data/screenshots"
all_files = os.listdir(screenshots_folder)

for filename in all_files:
    image_path = os.path.join(screenshots_folder, filename)
    detections = reader.readtext(image_path)

    text_fragments = [detection[1] for detection in detections]
    full_text = " ".join(text_fragments)

    timestamp = filename.replace(".png", "")

    cursor.execute("""
        INSERT INTO screenshots (filename, timestamp, ocr_text)
        VALUES (?, ?, ?)
    """, (filename, timestamp, full_text))

    print(f"Inserted: {filename}")

connection.commit()
connection.close()

print("All done.")