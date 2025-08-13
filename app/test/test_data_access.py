import asyncio
from data_access import PostgresClient, RedisClient

async def test_redis():
    rclient = RedisClient()
    test_bar = {
        "symbol": "btcusdt",
        "open_time": 1234567890,
        "open": 100,
        "high": 110,
        "low": 90,
        "close": 105,
        "volume": 1000,
        "close_time": 1234567999,
    }
    await rclient.set_bar(test_bar['symbol'], test_bar['open_time'], test_bar)
    retrieved = await rclient.get_bar(test_bar['symbol'], test_bar['open_time'])
    print("Redis retrieved bar:", retrieved)
    await rclient.close()

def test_postgres():
    pg = PostgresClient()
    test_bar = [{
        "symbol": "btcusdt",
        "open_time": 1234567890,
        "open": 100,
        "high": 110,
        "low": 90,
        "close": 105,
        "volume": 1000,
        "close_time": 1234567999,
    }]
    pg.insert_bars(test_bar)
    rows = pg.fetch_latest_bars("btcusdt", limit=5)
    print("Postgres latest bars:", rows)
    pg.close()

if __name__ == "__main__":
    test_postgres()
    asyncio.run(test_redis())
