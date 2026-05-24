import sqlite3

conn = sqlite3.connect("maternal.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
id INTEGER PRIMARY KEY AUTOINCREMENT,
maternal_id TEXT,
name TEXT,
age INTEGER,
contact TEXT,
address TEXT,
lmp TEXT,
hospital TEXT,
history TEXT,
risk TEXT DEFAULT 'Pending'
)
""")

conn.commit()
conn.close()

print("Updated Database")