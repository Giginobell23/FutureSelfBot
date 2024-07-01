import sqlite3
import aiosqlite

def initialize_database():
    with sqlite3.connect('email.db') as conn:
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            send_to TEXT NOT NULL,
            user_id TEXT NOT NULL,
            sent BOOLEAN DEFAULT 0,
            send_date DATETIME NOT NULL,
            subject VARCHAR(255) NOT NULL,
            body TEXT NOT NULL
            )
        ''')
        conn.commit()

async def retrieve_scheduled_emails(user_id):
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute("SELECT * FROM emails WHERE user_id = ? AND sent = 0", (user_id,))
            return await c.fetchall()
    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

async def insert_email_db(user_id, send_date,send_to, subject, body):
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute('INSERT INTO emails ( user_id, send_date, send_to, subject, body) VALUES ( ?, ?, ?, ?, ?)',(user_id, send_date, send_to, subject, body))
            await conn.commit()
    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

async def update_email_status(email_id):
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute("UPDATE emails SET sent = 1 WHERE id = ?", (email_id,))
            await conn.commit()
    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

async def retrieve_emails_for_today():
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute("SELECT * FROM emails WHERE strftime('%Y-%m-%d', send_date) = strftime('%Y-%m-%d', 'now') and sent = 0")
            return await c.fetchall()
    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

async def retrieve_email_by_id(email_id, user_id):
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute("SELECT * FROM emails WHERE id = ? and user_id = ? and sent = 0", (email_id,user_id))
            return await c.fetchone()
    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

async def get_emails_by_user_id(user_id):
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute("SELECT DISTINCT send_to FROM emails WHERE user_id = ?", (user_id,))
            return await c.fetchall()
    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

async def delete_email_by_id(email_id, user_id):
    conn = None
    try:
        conn = await aiosqlite.connect('email.db')
        async with conn.cursor() as c:
            await c.execute("DELETE FROM emails WHERE id = ? and user_id = ?", (email_id,user_id))
            await conn.commit()
            await c.execute("SELECT CASE WHEN changes() > 0 THEN 1 ELSE 0 END AS result;")
            return await c.fetchone()

    except aiosqlite.Error as e:
        print("Error occurred while database operation:", e)
    finally:
        if conn:
            await conn.close()

initialize_database()