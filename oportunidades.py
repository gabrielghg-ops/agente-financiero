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

    try:

        media50 = data["Close"].rolling(50).mean().iloc[-1].item()
        precio = data["Close"].iloc[-1].item()

    except Exception:
        print(f"{ticker} error calculando indicadores")
        return False

    if precio > media50:

        print(f"{ticker} tendencia alcista")

        return True

    print(f"{ticker} tendencia bajista")

    return False