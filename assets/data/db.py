import sqlite3, datetime, pytz, aiosqlite
from assets.config.cfg import PATH_DATABASE
from datetime import datetime

now = datetime.now()
conn=sqlite3.connect(PATH_DATABASE)
cursor = conn.cursor()
timezone = pytz.timezone('Europe/Kyiv')
time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M')

def add_user(user_id, user_name):
    data = cursor.execute(f'SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if data is None:
        sql = "INSERT INTO users (user_id, user_name, banned, reg_time) VALUES (?, ?, ?, ?)"
        val = (user_id, user_name, 0, time)
        cursor.execute(sql, val)
        conn.commit()
        return False
    else:
        pass
        return True

def add_post(post_id, post_title, post_text, post_link, m_id):
    sql = "INSERT INTO posts (post_id, post_title, post_text, post_link, add_time, m_id) VALUES (?, ?, ?, ?, ?, ?)"
    val = (post_id, post_title, post_text, post_link, time, m_id)
    cursor.execute(sql, val)
    conn.commit()

def get_post(m_id):
    c = cursor.execute('SELECT * FROM posts WHERE m_id = ?', (m_id,)).fetchone()
    return c[0] if c else None

def change_p_id(m_id, p_id):
    cursor.execute("UPDATE posts SET post_id = ? WHERE m_id = ?", (p_id, m_id,))
    conn.commit()

def check_ban(user_id):
    c = cursor.execute('SELECT banned FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return c[0] if c else None

def get_user(user_id):
    data = cursor.execute(f'SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return True if data else False

def get_code(code):
    c = cursor.execute('SELECT * FROM code_auth WHERE code = ?', (code,)).fetchone()
    return True if c else False

def get_work_sites():
    c = cursor.execute('SELECT site_name FROM sites WHERE status = 1').fetchall()
    return c

def delete_zav(m_id):
    cursor.execute('DELETE FROM posts WHERE m_id = ?', (m_id,))
    conn.commit()

def delete_post(post_id):
    cursor.execute('DELETE FROM posts WHERE post_id = ?', (post_id,))
    conn.commit()

def get_post_pid(post_id):
    c = cursor.execute('SELECT * FROM posts WHERE post_id = ?', (post_id,)).fetchone()
    return c[0] if c else None

async def create_tables_if_not_exist():
    async with aiosqlite.connect(PATH_DATABASE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, user_name TEXT, banned INTEGER, reg_time TEXT)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS code_auth
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS posts
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, post_id INTEGER, post_title TEXT,
                            post_text TEXT, post_link TEXT, add_time TEXT, m_id INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS sites
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, site_name TEXT NOT NULL UNIQUE, status INTEGER DEFAULT 0)''')
        await db.commit()