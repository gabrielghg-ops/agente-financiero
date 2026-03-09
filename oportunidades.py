import yfinance as yf


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

        precio = float(data["Close"].iloc[-1])
        ma50 = float(data["Close"].rolling(50).mean().iloc[-1])

    except Exception:

        print(f"{ticker} error calculando indicadores")
        return None

    if precio > ma50:
        signal = "alcista"
    else:
        signal = "bajista"

    return {
        "ticker": ticker,
        "price": round(precio,2),
        "ma50": round(ma50,2),
        "signal": signal
    }