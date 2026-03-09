import yfinance as yf
import pandas as pd


def analizar_activo(ticker):

    try:

        df = yf.download(ticker, period="6mo", progress=False)

        if df is None or df.empty:
            return None

        delta = df["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100/(1+rs))

        last_price = float(df["Close"].iloc[-1])
        last_rsi = float(rsi.iloc[-1])

        if last_rsi < 35:
            signal = "COMPRA"

        elif last_rsi > 70:
            signal = "VENTA"

        else:
            signal = "MANTENER"

        return {
            "ticker": ticker,
            "price": round(last_price,2),
            "rsi": round(last_rsi,1),
            "signal": signal
        }

    except:

        return None