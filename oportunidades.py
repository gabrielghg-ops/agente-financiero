import yfinance as yf
import pandas as pd


def descargar_datos(ticker):

    try:

        data = yf.download(ticker, period="6mo", progress=False)

        if data is None or data.empty:
            print(f"{ticker} sin datos")
            return None

        return data

    except Exception as e:

        print(f"{ticker} error descargando datos: {e}")
        return None


def analizar_activo(ticker):

    data = descargar_datos(ticker)

    if data is None:
        return None

    try:

        close = data["Close"]

        if len(close) < 50:
            print(f"{ticker} pocos datos")
            return None

        precio = close.iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if pd.isna(precio) or pd.isna(ma50):
            print(f"{ticker} datos incompletos")
            return None

        if precio > ma50:
            signal = "alcista"
        else:
            signal = "bajista"

        return {
            "ticker": ticker,
            "price": round(float(precio),2),
            "ma50": round(float(ma50),2),
            "signal": signal
        }

    except Exception as e:

        print(f"{ticker} error calculando indicadores:", e)
        return None