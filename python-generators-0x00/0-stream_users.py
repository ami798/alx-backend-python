#!/usr/bin/env python3
import sqlite3

def stream_users():
    """Generator that yields rows one by one from the user_data table."""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # This allows fetching rows as dict-like
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_data")

    for row in cur:
        yield dict(row)

    conn.close()
