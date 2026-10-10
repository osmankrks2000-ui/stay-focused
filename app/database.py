import os, sqlite3
from flask import current_app

DB = os.getenv('DATABASE_URL', 'stay_focused.db')

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db(app):
    with app.app_context():
        c = conn()
        c.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        c.commit(); c.close()

def add_lead(name, email, phone, message):
    c = conn(); c.execute('INSERT INTO leads(name,email,phone,message) VALUES(?,?,?,?)', (name,email,phone,message)); c.commit(); c.close()

def all_leads():
    c = conn(); rows = c.execute('SELECT * FROM leads ORDER BY created_at DESC').fetchall(); c.close()
    return [dict(r) for r in rows]
