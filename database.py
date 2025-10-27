import os
from fastapi import FastAPI
import aiomysql
from dotenv import load_dotenv  # opcional

load_dotenv()  # lee el archivo .env si existe

pool = None  # variable global


async def connect_to_db():
    global pool
    pool = await aiomysql.create_pool(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        db=os.environ.get("DB_NAME"),
        minsize=int(os.environ.get("DB_MIN", 1)),
        maxsize=int(os.environ.get("DB_MAX", 5)),
        autocommit=True,
    )
    print("Conectado a la base de datos")


async def close_db_connection():
    global pool
    pool.close()
    await pool.wait_closed()
    print("Conexión cerrada")


async def query(sql: str, params: tuple | None = None, one: bool = False):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, params)
            return await cur.fetchone() if one else await cur.fetchall()
