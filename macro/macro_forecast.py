import yfinance as yf
import pandas as pd


def _get_close_series(data):
    if data is None or data.empty:
        return pd.Series(dtype="float64")

    close = data["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return pd.to_numeric(close, errors="coerce").dropna()


def macro_forecast():
    spy = yf.download("SPY", period="3mo", interval="1d", progress=False)
    vix = yf.download("^VIX", period="3mo", interval="1d", progress=False)
    dxy = yf.download("DX-Y.NYB", period="3mo", interval="1d", progress=False)

    spy_close = _get_close_series(spy)
    vix_close = _get_close_series(vix)
    dxy_close = _get_close_series(dxy)

    if len(spy_close) < 2 or len(vix_close) == 0:
        return {
            "risk_on": 0.0,
            "neutral": 100.0,
            "risk_off": 0.0
        }

    spy_return = (float(spy_close.iloc[-1]) / float(spy_close.iloc[0])) - 1
    vix_level = float(vix_close.iloc[-1])

    risk_on = 50
    neutral = 30
    risk_off = 20

    if spy_return > 0.05:
        risk_on += 20
    elif spy_return > 0:
        risk_on += 10
    else:
        risk_off += 10

    if vix_level > 25:
        risk_off += 20
        risk_on -= 10
    elif vix_level < 18:
        risk_on += 10

    if len(dxy_close) >= 2:
        dxy_return = (float(dxy_close.iloc[-1]) / float(dxy_close.iloc[0])) - 1
        if dxy_return > 0.03:
            risk_off += 10
        elif dxy_return < -0.02:
            risk_on += 10

    risk_on = max(risk_on, 0)
    neutral = max(neutral, 0)
    risk_off = max(risk_off, 0)

    total = risk_on + neutral + risk_off

    return {
        "risk_on": round(risk_on / total * 100, 1),
        "neutral": round(neutral / total * 100, 1),
        "risk_off": round(risk_off / total * 100, 1)
    }