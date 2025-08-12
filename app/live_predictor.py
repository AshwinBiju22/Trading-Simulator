import joblib
from data_access import PostgresClient
from feature_engineering import bars_to_df, add_features
import pandas as pd

class LivePredictor:
    def __init__(self, model_path, symbol, window=100):
        self.model = joblib.load(model_path)
        self.symbol = symbol
        self.window = window
        self.pg = PostgresClient()

    def predict_next_close(self):
        bars = self.pg.fetch_latest_bars(self.symbol, limit=self.window)
        df = bars_to_df(bars)
        df = add_features(df)

        # We want to predict next close based on the most recent row's features
        latest_features = df.iloc[-1][['close', 'ma5', 'ma10', 'volatility']].to_frame().T
        prediction = self.model.predict(latest_features)
        return prediction[0]

    def close(self):
        self.pg.close()

if __name__ == "__main__":
    predictor = LivePredictor("C:/Users/ashwi/OneDrive/Documents/1_UNI/Projects/Real-Time Market Data Trading Simulator/Trading-Simulator/app/rf_model.joblib", "btcusdt")
    pred = predictor.predict_next_close()
    print(f"Predicted next close price: {pred:.2f}")
    predictor.close()