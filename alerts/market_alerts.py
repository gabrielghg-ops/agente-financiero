import yfinance as yf
import pandas as pd


def _get_close_series(data):
    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def revisar_alertas():

    alertas = []

    activos = [
        "SPY",
        "^VIX",
        "GLD",
        "SLV",
        "EEM"
    ]

    for ticker in activos:

        try:

            data = yf.download(
                ticker,
                period="6mo",
                interval="1d",
                progress=False
            )

            close = _get_close_series(data)

            if len(close) < 20:
                continue

            precio = float(close.iloc[-1])
            ma20 = close.rolling(20).mean().iloc[-1]

            if pd.notna(ma20):

                if precio > ma20 * 1.05:
                    alertas.append(f"{ticker} fuerte momentum alcista")

                elif precio < ma20 * 0.95:
                    alertas.append(f"{ticker} debilidad significativa")

        except Exception as e:

            print(f"Error alertas {ticker}: {e}")

    if len(alertas) == 0:
        return None

    return "\n".join(alertas)