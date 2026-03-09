import yfinance as yf
import pandas as pd

# conversión de tickers locales a Yahoo
TICKER_MAP = {
"YPFD": "YPF",
"PAMP": "PAMP.BA",
"BYMA": "BYMA.BA",
"GGAL": "GGAL.BA",
"CEPU": "CEPU.BA",
"LOMA": "LOMA.BA",
}

def convertir_ticker(t):

    if t in TICKER_MAP:
        return TICKER_MAP[t]

    return t


def analizar_activo(ticker):

    ticker = convertir_ticker(ticker)

    df = yf.download(ticker, period="6mo")

    if df.empty:
        return None

    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

    rs = gain / loss
    rsi = 100 - (100/(1+rs))

    last = df.iloc[-1]

    if rsi.iloc[-1] < 35:
        signal = "🟢 COMPRA"
    elif rsi.iloc[-1] > 70:
        signal = "🔴 VENTA"
    else:
        signal = "🟡 MANTENER"

    return {
        "ticker": ticker,
        "price": round(last["Close"],2),
        "rsi": round(rsi.iloc[-1],1),
        "signal": signal
    }