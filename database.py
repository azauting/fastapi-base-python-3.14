import aiomysql
from fastapi import FastAPI

pool = None  # variable global

async def connect_to_db():
    global pool
    pool = await aiomysql.create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="",
        db="hosptest1",
        minsize=1,
        maxsize=5,
    )

async def close_db_connection():
    global pool
    pool.close()
    await pool.wait_closed()
    
async def query(sql: str, params: tuple | None = None, one: bool = False):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, params)
            return await cur.fetchone() if one else await cur.fetchall()
