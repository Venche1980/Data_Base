# database.py
import psycopg2
from contextlib import contextmanager
from config import DB_CONFIG  # Import the database configuration

@contextmanager
def connect_db():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def fetch_word(cid):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT word_en, word_ru FROM Words 
            WHERE word_en NOT IN (
                SELECT word_en FROM UserWords WHERE user_id = %s
            ) ORDER BY RANDOM() LIMIT 1
        """, (cid,))
        return cur.fetchone()

def fetch_random_words(exclude_word, limit=3):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT word_en FROM (
                SELECT DISTINCT word_en FROM Words WHERE word_en != %s
            ) AS distinct_words
            ORDER BY RANDOM() LIMIT %s
        """, (exclude_word, limit))
        return [row[0] for row in cur.fetchall()]

def insert_user_word(cid, word_en, word_ru):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING", (cid,))
        cur.execute("INSERT INTO UserWords (user_id, word_en, word_ru) VALUES (%s, %s, %s)", (cid, word_en, word_ru))
        conn.commit()

def delete_user_word(cid, word_en):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM UserWords WHERE user_id = %s AND word_en = %s", (cid, word_en))
        conn.commit()

# Add more database functions as needed
