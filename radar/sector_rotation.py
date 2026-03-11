import yfinance as yf
import pandas as pd

SECTORS = {
    "Tecnologia": "XLK",
    "Finanzas": "XLF",
    "Energia": "XLE",
    "Salud": "XLV",
    "Industria": "XLI",
    "Consumo": "XLY",
    "Defensivo": "XLP"
}


def _get_close_series(data):
    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def sector_rotation():
    results = {}

    for sector, ticker in SECTORS.items():
        try:
            data = yf.download(ticker, period="3mo", interval="1d", progress=False)
            close = _get_close_series(data)

            if len(close) < 2:
                continue

            perf = (float(close.iloc[-1]) / float(close.iloc[0])) - 1
            results[sector] = round(perf * 100, 2)

        except Exception as e:
            print(f"Error sector {sector}: {e}")

    return sorted(results.items(), key=lambda x: x[1], reverse=True)