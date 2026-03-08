import yfinance as yf
import pandas as pd

def rsi(series, period=14):

    delta = series.diff()

    gain = (delta.where(delta > 0, 0)).rolling(period).mean()

    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss

    return 100 - (100/(1+rs))


def analizar_activo(ticker):

    df = yf.download(ticker, period="6mo")

    df["RSI"] = rsi(df["Close"])

    last = df.iloc[-1]

    if last["RSI"] < 35:

        signal = "🟢 COMPRA"

    elif last["RSI"] > 70:

        signal = "🔴 VENTA"

    else:

        signal = "🟡 MANTENER"

    return {
        "ticker": ticker,
        "price": round(last["Close"],2),
        "rsi": round(last["RSI"],1),
        "signal": signal
    }