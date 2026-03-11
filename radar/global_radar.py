import yfinance as yf
import pandas as pd

ACTIVOS_RADAR = {
    "SPY": "USA",
    "EEM": "Emergentes",
    "EWZ": "Brasil",
    "GLD": "Oro",
    "SLV": "Plata",
    "XLK": "Tecnologia",
    "IBIT": "Bitcoin ETF"
}


def _get_close_series(data):
    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def radar_global():
    resultados = []

    for ticker, nombre in ACTIVOS_RADAR.items():
        try:
            data = yf.download(ticker, period="3mo", interval="1d", progress=False)
            close = _get_close_series(data)

            if len(close) < 2:
                continue

            precio = float(close.iloc[-1])
            ma50 = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
            rendimiento = ((precio / float(close.iloc[0])) - 1) * 100

            if ma50 is not None and pd.notna(ma50):
                sesgo = "alcista" if precio > float(ma50) else "bajista"
            else:
                sesgo = "sin señal"

            resultados.append(
                f"{ticker} ({nombre}) | {round(rendimiento, 2)}% | {sesgo}"
            )

        except Exception as e:
            print(f"Error radar {ticker}: {e}")

    if not resultados:
        return "Sin datos disponibles"

    return "\n".join(resultados)