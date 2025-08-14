from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from data_access import PostgresClient, RedisClient
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production to your UI domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

pg = PostgresClient()
redis = RedisClient()


#@app.get("/")
#def serve_dashboard():
#    return FileResponse("C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/templates/dashboard.html")


# Serve landing page
@app.get("/")
def serve_landing():
    return FileResponse("C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/templates/index.html")

# Serve live data dashboard
@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/templates/dashboard.html")

# Serve predictions page
@app.get("/predictions")
def serve_predictions():
    return FileResponse("C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/templates/predictions.html")

# API: fetch recent bars
@app.get("/bars")
def get_bars(symbol: str = "btcusdt", limit: int = 100):
    return pg.fetch_latest_bars(symbol, limit)

# API: fetch latest prediction
@app.get("/prediction")
async def get_prediction(symbol: str = "btcusdt"):
    key = f"prediction:{symbol}:next_close"
    prediction = await redis.get(key)
    if prediction is not None:
        return {"next_close": float(prediction)}
    return {"next_close": None}

@app.get("/predictions-data")
async def get_predictions_data(symbol: str = "btcusdt", limit: int = 100):
    # Get recent bars
    bars = pg.fetch_latest_bars(symbol, limit)
    timestamps = [bar["timestamp"] for bar in bars]
    prices = [bar["close"] for bar in bars]

    # Get historical predictions
    preds = []
    for ts in timestamps:
        key = f"prediction:{symbol}:{ts}"
        pred = await redis.get(key)
        preds.append(float(pred) if pred is not None else None)

    return {
        "timestamps": timestamps,
        "prices": prices,
        "predictions": preds
    }

