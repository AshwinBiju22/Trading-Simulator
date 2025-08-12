import joblib
from data_access import PostgresClient
from feature_engineering import bars_to_df, add_features
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_model(symbol="btcusdt"):
    pg = PostgresClient()
    bars = pg.fetch_latest_bars(symbol, limit=2000)
    pg.close()

    df = bars_to_df(bars)
    df = add_features(df)

    # Target: next bar's close price
    df['target'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    features = ['close', 'ma5', 'ma10', 'volatility']
    X = df[features]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    print(f"Test MSE: {mse:.6f}")

    joblib.dump(model, "rf_model.joblib")
    print("Model saved as rf_model.joblib")

if __name__ == "__main__":
    train_model()
