from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data_access import PostgresClient, RedisClient
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production to your UI domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pg = PostgresClient()
redis = RedisClient()

@app.get("/bars")
def get_bars(symbol: str = "btcusdt", limit: int = 100):
    bars = pg.fetch_latest_bars(symbol, limit)
    return bars

@app.get("/prediction")
async def get_prediction(symbol: str = "btcusdt"):
    key = f"prediction:{symbol}:next_close"
    prediction = await redis.get(key)
    if prediction is not None:
        return {"next_close": float(prediction)}
    return {"next_close": None}
