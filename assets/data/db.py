import aiomysql
import datetime
import pytz
from datetime import datetime

timezone = pytz.timezone('Europe/Kyiv')
time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M')

async def get_connection():
    return await aiomysql.connect(
        host='localhost',
        port=3306,
        user='fxaiwwky_admin',
        password='dHj[3uYxY8K23(',
        db='fxaiwwky_news',
        autocommit=True
    )

async def add_user(user_id, user_name):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
        data = await cursor.fetchone()
        if data is None:
            sql = "INSERT INTO users (user_id, user_name, banned, reg_time) VALUES (%s, %s, %s, %s)"
            val = (user_id, user_name, 0, time)
            await cursor.execute(sql, val)
            return False
        else:
            return True

async def add_code(code):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        sql = "INSERT INTO code_auth (code) VALUES (%s)"
        val = (code)
        await cursor.execute(sql, val)

async def add_post(post_id, post_title, post_text, post_link, m_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM posts WHERE post_title=%s", (post_title,))
        if not await cursor.fetchone():
            sql = "INSERT INTO posts (post_id, post_title, post_text, post_link, add_time, m_id) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (post_id, post_title, post_text, post_link, time, m_id)
            await cursor.execute(sql, val)
            return True
    return False

async def get_post(m_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT * FROM posts WHERE m_id = %s', (m_id,))
        c = await cursor.fetchone()
        return c[0] if c else None

async def change_p_id(m_id, p_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("UPDATE posts SET post_id = %s WHERE m_id = %s", (p_id, m_id,))

async def change_m_id(m_id, title):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("UPDATE posts SET m_id = %s WHERE post_title = %s", (m_id, title,))

async def check_ban(user_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT banned FROM users WHERE user_id = %s', (user_id,))
        c = await cursor.fetchone()
        return c[0] if c else None

async def get_user(user_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
        data = await cursor.fetchone()
        return True if data else False

async def get_code(code):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT * FROM code_auth WHERE code = %s', (code,))
        c = await cursor.fetchone()
        return True if c else False

async def get_work_sites():
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT site_name FROM sites WHERE status = 1')
        c = await cursor.fetchall()
        return c

async def delete_zav(m_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('DELETE FROM posts WHERE m_id = %s', (m_id,))

async def delete_post(post_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('DELETE FROM posts WHERE post_id = %s', (post_id,))

async def get_post_pid(post_id):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('SELECT * FROM posts WHERE post_id = %s', (post_id,))
        c = await cursor.fetchone()
        return c[0] if c else None

async def create_tables_if_not_exist():
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INTEGER PRIMARY KEY AUTO_INCREMENT, user_id BIGINT, user_name TEXT, banned INTEGER, reg_time TEXT)''')
        await cursor.execute('''CREATE TABLE IF NOT EXISTS code_auth
                                (id INTEGER PRIMARY KEY AUTO_INCREMENT, code TEXT)''')
        await cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                                (id INTEGER PRIMARY KEY AUTO_INCREMENT, post_id INTEGER, post_title TEXT,
                                post_text TEXT, post_link TEXT, add_time TEXT, m_id INTEGER)''')
        await cursor.execute('''CREATE TABLE IF NOT EXISTS sites
                                (id INTEGER PRIMARY KEY AUTO_INCREMENT, site_name VARCHAR(255) NOT NULL UNIQUE, status INTEGER DEFAULT 0)''')