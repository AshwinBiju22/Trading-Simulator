import os
from dotenv import load_dotenv
import asyncio
import json
import redis.asyncio as redis  # <-- modern Redis client
import psycopg2
from psycopg2.extras import execute_values
import websockets

load_dotenv()

REDIS_URL = "redis://localhost"
PG_CONN_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "localhost",
    "port": 5432,
}

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{}@kline_{}"
SYMBOL = "btcusdt"
INTERVAL = "1m"

async def store_bar_pg(conn, bar):
    with conn.cursor() as cur:
        sql = """
        INSERT INTO crypto_bars (symbol, open_time, open, high, low, close, volume, close_time)
        VALUES %s
        ON CONFLICT (symbol, open_time) DO NOTHING
        """
        values = [(
            bar['symbol'],
            bar['open_time'],
            bar['open'],
            bar['high'],
            bar['low'],
            bar['close'],
            bar['volume'],
            bar['close_time']
        )]
        execute_values(cur, sql, values)
    conn.commit()

async def main():
    redis_client = redis.from_url(REDIS_URL)
    pg_conn = psycopg2.connect(**PG_CONN_PARAMS)

    ws_url = BINANCE_WS_URL.format(SYMBOL, INTERVAL)
    try:
        async with websockets.connect(ws_url) as websocket:
            print(f"Connected to Binance websocket for {SYMBOL} {INTERVAL} bars.")
            async for message in websocket:
                msg = json.loads(message)
                kline = msg['k']

                bar = {
                    "symbol": SYMBOL,
                    "open_time": kline['t'],
                    "open": float(kline['o']),
                    "high": float(kline['h']),
                    "low": float(kline['l']),
                    "close": float(kline['c']),
                    "volume": float(kline['v']),
                    "close_time": kline['T']
                }

                # Store in Redis
                redis_key = f"bar:{SYMBOL}:{bar['open_time']}"
                await redis_client.set(redis_key, json.dumps(bar))

                # Store in Postgres
                await store_bar_pg(pg_conn, bar)

                print(f"Stored bar for {SYMBOL} @ {bar['open_time']} Close: {bar['close']}")

    except asyncio.CancelledError:
        print("Task was cancelled, cleaning up...")

    except KeyboardInterrupt:
        print("\nReceived exit signal. Closing connections...")

    finally:
        # Close Redis client properly
        await redis_client.aclose()
        # Close PostgreSQL connection
        pg_conn.close()
        print("Shutdown complete. Bye!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # This catches Ctrl+C during asyncio.run if it bubbles up
        print("\nProgram interrupted. Exiting cleanly.")
