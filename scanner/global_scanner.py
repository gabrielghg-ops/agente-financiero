import yfinance as yf
import pandas as pd

ASSETS = [
    "NVDA","MSFT","AAPL","META","AMD",
    "GLD","SLV","COPX","URA",
    "XLE","XLK","EEM","EWZ","IBIT"
]


def _get_close(data):

    if data is None or data.empty:
        return pd.Series(dtype="float64")

    c = data["Close"]

    if isinstance(c, pd.DataFrame):
        c = c.iloc[:,0]

    return pd.to_numeric(c, errors="coerce").dropna()


def scan_assets():

    resultados = []

    for ticker in ASSETS:

        try:

            data = yf.download(
                ticker,
                period="12mo",
                interval="1d",
                progress=False
            )

            close = _get_close(data)

            if len(close) < 50:
                continue

            precio = float(close.iloc[-1])

            ma50 = close.rolling(50).mean().iloc[-1]

            momentum = (precio / float(close.iloc[-60])) - 1

            score = 0

            if precio > ma50:
                score += 3

            if momentum > 0:
                score += 3

            if momentum > 0.10:
                score += 2

            if momentum > 0.20:
                score += 2

            resultados.append((ticker, score))

        except Exception as e:

            print("scanner error", ticker, e)

    resultados = sorted(resultados, key=lambda x: x[1], reverse=True)

    return resultados[:5]