import asyncio
import json
import websockets
from data_access import PostgresClient, RedisClient
from live_predictor import LivePredictor

SYMBOL = "btcusdt"
INTERVAL = "1m"
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/{}@kline_{}"

async def main():
    pg_client = PostgresClient()
    redis_client = RedisClient()
    predictor = LivePredictor("C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/rf_model.joblib", SYMBOL)

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

                # Store bar in Postgres (list for insert_bars API)
                pg_client.insert_bars([bar])

                # Store bar in Redis
                await redis_client.set_bar(SYMBOL, bar['open_time'], bar)

                print(f"Stored bar for {SYMBOL} @ {bar['open_time']} Close: {bar['close']}")

                 # Make live prediction
                try:
                    pred_close = predictor.predict_next_close()
                    print(f"Predicted next close price: {pred_close:.2f}")

                    # Save prediction to Redis for UI/API to access
                    key = f"prediction:{SYMBOL}:next_close"
                    await redis_client.set(key, pred_close)

                except Exception as e:
                    print(f"Prediction error: {e}")

    except asyncio.CancelledError:
        print("Task was cancelled, cleaning up...")

    except KeyboardInterrupt:
        print("\nReceived exit signal. Closing connections...")

    finally:
        await redis_client.close()
        pg_client.close()
        predictor.close()
        print("Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting cleanly.")
