import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/sisac.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            accion TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_audit(usuario, accion):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO auditoria (usuario, accion) VALUES (?,?)", (usuario, accion))
    conn.commit()
    conn.close()
