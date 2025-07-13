import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
''')

cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Amira", "amira@example.com"))
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John", "john@example.com"))
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Lina", "lina@example.com"))

conn.commit()
conn.close()

print("✅ Database and users table created with sample data.")
