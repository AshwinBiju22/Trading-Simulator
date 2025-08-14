# QuantFlow – Real-Time Trading Simulator
---
## Overview  
QuantFlow is a **full-stack real-time trading simulator** designed for quantitative analysis and market research.  
It integrates **live cryptocurrency market data** from Binance, **ML-driven forecasting**, and **interactive analytics** into a professional web interface.  

Developed as a personal quantitative research platform, it combines **low-latency backend pipelines** with **modern frontend visualizations** to deliver an institutional-grade trading environment.  

---

## Video Demonstration

Demo : In Progress

---

## Features  

### Real-Time Market Data Feed  
- Streams live BTCUSDT price data via Binance WebSocket API.  
- PostgreSQL for historical data storage and retrieval.  
- Redis for ultra-fast in-memory caching of latest ticks and predictions.  

---

### AI-Powered Price Forecasting  
- **Model:** Random Forest Regressor trained on engineered market features.  
- Predicts the **next price close** in real time.  
- Automated retraining workflow keeps predictions updated with latest market conditions.  

**Feature Engineering Highlights:**  
- Rolling averages, price momentum, volatility indicators.  
- Normalization and outlier handling.  

---

### Interactive Web Dashboard  
- Built with **TailwindCSS** for a sleek UI.  
- **Chart.js** for live candlestick and line charts.  
- Three main pages:  
  - **Home:** Professional landing page with platform overview.  
  - **Live Data:** Real-time price chart with second-by-second updates.  
  - **Predictions:** Side-by-side view of actual vs. predicted prices.  

---

## System Architecture  

```
Binance WebSocket → Data Collector → PostgreSQL & Redis
                                   ↓
                           Feature Engineering
                                   ↓
                          Random Forest Model
                                   ↓
                          WebSocket API → Frontend
```

---

## Tech Stack  

- **Backend:** Python, FastAPI, WebSockets, PostgreSQL, Redis, Scikit-learn, Pandas, NumPy  
- **Frontend:** HTML5, TailwindCSS, Chart.js, JavaScript  
- **Data Source:** Binance API (WebSocket + REST)  
- **Infrastructure:** Local/PostgreSQL DB, Redis Cache, environment-managed secrets  

