import sqlite3

DB_NAME = "inventario.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            stock INTEGER NOT NULL DEFAULT 0,
            purchase_price REAL NOT NULL,
            sale_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movements (
            id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL,
            type TEXT CHECK(type IN ('purchase', 'sale')) NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()