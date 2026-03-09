import yfinance as yf
import pandas as pd


def descargar_datos(ticker):

    try:

        data = yf.download(
            ticker,
            period="6mo",
            auto_adjust=True,
            progress=False
        )

        if data is None or data.empty:
            print(f"{ticker} sin datos")
            return None

        return data

    except Exception as e:

        print(f"{ticker} error descargando datos: {e}")
        return None


def obtener_close(data):

    try:

        close = data["Close"]

        # si yfinance devuelve dataframe en vez de serie
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        return close.dropna()

    except Exception:
        return None


def analizar_activo(ticker):

    data = descargar_datos(ticker)

    if data is None:
        return None

    close = obtener_close(data)

    if close is None or len(close) < 50:
        print(f"{ticker} pocos datos")
        return None

    try:

        precio = float(close.iloc[-1])
        ma50 = float(close.rolling(50).mean().iloc[-1])

    except Exception as e:

        print(f"{ticker} error calculando indicadores:", e)
        return None

    if pd.isna(precio) or pd.isna(ma50):
        print(f"{ticker} datos incompletos")
        return None

    signal = "alcista" if precio > ma50 else "bajista"

    return {
        "ticker": ticker,
        "price": round(precio, 2),
        "ma50": round(ma50, 2),
        "signal": signal
    }