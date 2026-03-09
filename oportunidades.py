import yfinance as yf


def descargar_datos(ticker):

    try:

        data = yf.download(ticker, period="6mo", progress=False)

        if data.empty:
            return None

        return data

    except Exception:
        return None


def analizar_activo(ticker):

    data = descargar_datos(ticker)

    if data is None:

        print(f"{ticker} sin datos")

        return False

    media50 = data["Close"].rolling(50).mean().iloc[-1]
    precio = data["Close"].iloc[-1]

    if precio > media50:

        return True

    return False