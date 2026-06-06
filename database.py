import sqlite3
import os
import hashlib

DB_DIR = 'data'
DB_PATH = os.path.join(DB_DIR, 'deadlines.db')

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            subject TEXT DEFAULT '',
            deadline TEXT NOT NULL,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'current'
        );
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            unlocked INTEGER DEFAULT 0
        );
    ''')
    
    achievements = [
        ('first_task', 'Первый шаг', 'Создана первая учебная задача'),
        ('done_5', 'Отличник', 'Выполнено 5 задач'),
        ('no_overdue', 'В дедлайне', 'Нет просроченных задач')
    ]
    for code, title, desc in achievements:
        try:
            cursor.execute('INSERT INTO achievements (code, title, description) VALUES (?, ?, ?)', (code, title, desc))
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def has_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def register_user(password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hp = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', ('student', hp))
    conn.commit()
    conn.close()

def check_user(password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hp = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute('SELECT id FROM users WHERE login = ? AND password = ?', ('student', hp))
    user = cursor.fetchone()
    conn.close()
    return user is not None