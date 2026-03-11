import yfinance as yf
import pandas as pd

def detect_crash_risk():

    spy = yf.download("SPY", period="6mo", interval="1d")
    vix = yf.download("^VIX", period="6mo", interval="1d")

    spy["MA50"] = spy["Close"].rolling(50).mean()
    spy["MA200"] = spy["Close"].rolling(200).mean()

    spy_price = spy["Close"].iloc[-1]
    ma50 = spy["MA50"].iloc[-1]
    ma200 = spy["MA200"].iloc[-1]

    vix_value = vix["Close"].iloc[-1]

    score = 0

    if spy_price < ma50:
        score += 30

    if spy_price < ma200:
        score += 40

    if vix_value > 30:
        score += 30

    if score < 30:
        level = "BAJO"
    elif score < 60:
        level = "MEDIO"
    else:
        level = "ALTO"

    return {
        "crash_score": score,
        "crash_risk": level
    }