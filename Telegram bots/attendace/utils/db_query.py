import asyncpg
from datetime import datetime, time, date
from zoneinfo import ZoneInfo
from credentials import USER, PASSWORD, DATABASE

async def connection():
    connect = await asyncpg.connect(
        user='postgres',
        password=PASSWORD,
        database=DATABASE,
        host='localhost'
    )
    return connect
    
async def create_user(chat_id: int, first_name: str, username: str):
    conn = await connection()
    await conn.execute(
        "INSERT INTO users(chat_id, first_name, username, created_at) VALUES ($1, $2, $3, $4) RETURNING id, number_of_late;",
        chat_id, first_name, username, datetime.now(ZoneInfo("Asia/Tashkent"))
    )
    await conn.close()
    
async def get_user(chat_id: int):
    conn = await connection()
    try:
        user = await conn.fetchrow(
            'SELECT * FROM users WHERE chat_id=$1', 
            chat_id
        )
        return user
    finally:
        await conn.close()
        
async def create_arrival(chat_id: int, arrival_time: time, early_minutes: time = 0, late_minutes: time = 0):
    conn = await connection()
    await conn.execute(
        "INSERT INTO attendances(chat_id, arrival_time, day, early_minutes, delayed_minutes) VALUES($1, $2, $3, $4, $5)",
        chat_id, arrival_time, datetime.today().date(), early_minutes, late_minutes
    )
    
    user = await conn.fetchrow(
        "SELECT number_of_late FROM users WHERE chat_id = $1;",
        chat_id
    )
    
    if late_minutes != 0:
        update_number_of_late = await conn.execute(
            """  
            UPDATE users
            SET number_of_late = $1 
            WHERE chat_id = $2;
        """,
            user['number_of_late'] + 1, chat_id, 
        )
        await conn.close()
    
async def create_leave(chat_id: int, leave_time: time, day: date):
    conn = await connection()
    await conn.execute(
        "UPDATE attendances SET leave_time=$1 WHERE chat_id=$2 AND day=$3",
        leave_time, chat_id, day
    )
    await conn.close()
    
async def check_attendance(chat_id: int, day: date):
    conn = await connection()
    attendance = await conn.fetchrow(
        "SELECT * FROM attendances WHERE chat_id=$1 AND day=$2",
        chat_id, day
    )
    await conn.close()
    return attendance

async def get_arrived_users(day: date):
    conn = await connection()
    users = await conn.fetch(
        """
        SELECT u.first_name, a.arrival_time
        FROM users u
        JOIN attendances a ON u.chat_id = a.chat_id
        WHERE u.is_admin = FALSE
        AND a.day = $1
        ORDER BY a.arrival_time ASC;    
        """,
        day
    )
    await conn.close()
    return users

async def get_missing_users(day: date):
    conn = await connection()
    users = await conn.fetch(
        """
        SELECT u.first_name 
        FROM users u
        LEFT JOIN attendances a 
        ON u.chat_id = a.chat_id
        AND a.day = $1 
        WHERE a.chat_id IS NULL
        AND u.is_admin = FALSE; 
        """,
        day
    )
    
    await conn.close()
    return users

async def get_remaining_users(day: date):
    conn = await connection()
    users = await conn.fetch(
        """
        SELECT u.first_name 
        FROM users u
        JOIN attendances a ON u.chat_id = a.chat_id
        WHERE a.day=$1 
        AND u.is_admin = FALSE 
        AND a.leave_time is NULL;
        """,
        day
    )
    await conn.close()
    return users

async def get_delayed_times():
    conn = await connection()
    delayed_times = await conn.fetch(
        """
        SELECT * FROM users
        WHERE number_of_late != 0;
        """
    )
    await conn.close()
    return delayed_times

async def update_user_penalty(chat_id: int, penalty_amount: int):
    conn = await connection()
    await conn.execute(
        """
        UPDATE users 
        SET number_of_late = $1
        WHERE chat_id = $2;
        """,
        penalty_amount, chat_id
    )
    await conn.close()

async def update_delayed_times():
    conn = await connection()
    query = await conn.execute(
        """
        UPDATE users 
        SET number_of_late = 0
        WHERE number_of_late != 0
        """
    )
    await conn.close()

async def create_morning_activity(chat_id: int, activity_time: datetime):
    conn = await connection()
    await conn.execute(
        "INSERT INTO morning_activity(chat_id, video_note_time) VALUES($1, $2)",
        chat_id, activity_time
    )
    await conn.close()

async def get_unpersistent_users(day: date):
    conn = await connection()
    users = await conn.fetch(
        """
        SELECT u.first_name
        FROM users u
        LEFT JOIN morning_activity m
        ON u.chat_id = m.chat_id
        WHERE m.chat_id IS NULL;
        """,
        day
    )
    await conn.close()
    return users

async def get_persistent_users():
   conn = await connection()
   users = await conn.fetch(
       """
       SELECT 
        u.first_name,
        COUNT(ma.id) AS total_days
        FROM morning_activity ma
        JOIN users u ON u.chat_id = ma.chat_id
        WHERE date_trunc('month', ma.video_note_time) = date_trunc('month', CURRENT_DATE)
        GROUP BY u.first_name
        ORDER BY total_days DESC;
    """
   )
   await conn.close()
   return users