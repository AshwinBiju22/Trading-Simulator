import os
import json
import redis.asyncio as redis
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = "redis://localhost"
PG_CONN_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "localhost",
    "port": 5432,
}

class PostgresClient:
    def __init__(self):
        self.conn = psycopg2.connect(**PG_CONN_PARAMS)

    def insert_bars(self, bars):
        with self.conn.cursor() as cur:
            sql = """
            INSERT INTO crypto_bars (symbol, open_time, open, high, low, close, volume, close_time)
            VALUES %s
            ON CONFLICT (symbol, open_time) DO NOTHING
            """
            values = [(b['symbol'], b['open_time'], b['open'], b['high'], b['low'], b['close'], b['volume'], b['close_time']) for b in bars]
            execute_values(cur, sql, values)
        self.conn.commit()

    def fetch_latest_bars(self, symbol, limit=100):
        with self.conn.cursor() as cur:
            sql = """
            SELECT symbol, open_time, open, high, low, close, volume, close_time
            FROM crypto_bars
            WHERE symbol = %s
            ORDER BY open_time DESC
            LIMIT %s
            """
            cur.execute(sql, (symbol, limit))
            rows = cur.fetchall()
            keys = ['symbol', 'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time']
            return [dict(zip(keys, row)) for row in rows]

    def close(self):
        self.conn.close()


class RedisClient:
    def __init__(self):
        self.client = redis.from_url(REDIS_URL)

    async def set_bar(self, symbol, open_time, bar):
        key = f"bar:{symbol}:{open_time}"
        await self.client.set(key, json.dumps(bar))

    async def get_bar(self, symbol, open_time):
        key = f"bar:{symbol}:{open_time}"
        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None

    async def close(self):
        await self.client.aclose()
